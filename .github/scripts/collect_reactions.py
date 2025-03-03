#!/usr/bin/env python3

import os
import json
import time
import re
import requests
from github import Github
from datetime import datetime, timedelta

# Initialize GitHub client
token = os.environ.get("GITHUB_TOKEN")
repo_name = os.environ.get("REPO")
specific_release = os.environ.get("SPECIFIC_RELEASE")
g = Github(token)
repo = g.get_repo(repo_name)

def extract_morphosource_data(release_body):
    """Extract the original MorphoSource release tag from the analysis release body"""
    match = re.search(r'Analysis for MorphoSource release: (morphosource-updates-[^\s]+)', release_body)
    if match:
        return match.group(1)
    return None

def get_morphosource_release(ms_tag):
    """Get the original MorphoSource release data"""
    try:
        release = repo.get_release(ms_tag)
        return release.body
    except:
        print(f"Could not find MorphoSource release with tag: {ms_tag}")
        return None

def extract_ct_analysis(release_body, release_type):
    """Extract the CT analysis text from the release body"""
    # Remove the header section that references MorphoSource
    clean_body = re.sub(r'Analysis for MorphoSource release: [^\n]+\n+', '', release_body)
    
    if release_type == "3d":
        # Remove the orientation views section for 3D analysis
        clean_body = re.sub(r'### Orientation Views[\s\S]+', '', clean_body)
    
    return clean_body.strip()

def create_fine_tuning_entry(morphosource_data, ct_analysis, is_preferred=True):
    """Create a fine-tuning entry in the expected format"""
    entry = {
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": morphosource_data
                }
            ],
            "tools": [],
            "parallel_tool_calls": True
        }
    }
    
    # Create the preferred and non-preferred outputs
    ct_output = {
        "role": "assistant",
        "content": ct_analysis
    }
    
    # Create a simplified/generic version for the alternative output
    simplified_output = {
        "role": "assistant",
        "content": "This CT scan shows anatomical structures typical for this species."
    }
    
    if is_preferred:
        entry["preferred_output"] = [ct_output]
        entry["non_preferred_output"] = [simplified_output]
    else:
        entry["preferred_output"] = [simplified_output]
        entry["non_preferred_output"] = [ct_output]
    
    return entry

def save_reaction_data(release_id, reaction_data):
    """Save reaction data to JSONL file, but only if there are reactions"""
    if not reaction_data:
        print(f"No reaction data to save for release {release_id}")
        return
        
    os.makedirs("data/reactions/jsonl", exist_ok=True)
    output_file = f"data/reactions/jsonl/release-{release_id}.jsonl"
    
    # Write to JSONL file
    with open(output_file, 'w') as f:
        for user, entry in reaction_data.items():
            f.write(json.dumps(entry) + '\n')
    
    print(f"Saved {len(reaction_data)} reactions to {output_file}")
    
    # Only write timestamp file if we actually saved reactions
    if reaction_data:
        with open("data/reactions/last_processed.txt", 'w') as f:
            f.write(datetime.now().isoformat())

def get_release_reactions(release_id):
    """Get reactions for a specific release using GitHub API"""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.squirrel-girl-preview+json"
    }
    
    api_url = f"https://api.github.com/repos/{repo_name}/releases/{release_id}/reactions"
    response = requests.get(api_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching reactions: {response.status_code} - {response.text}")
        return []
        
    return response.json()

# Set up our search criteria for releases
if specific_release:
    print(f"Checking specific release: {specific_release}")
    try:
        releases_to_check = [repo.get_release(specific_release)]
    except:
        print(f"Could not find release with ID: {specific_release}")
        releases_to_check = []
else:
    # Get releases from the last 30 days
    cutoff_date = datetime.now() - timedelta(days=30)
    all_releases = list(repo.get_releases())
    releases_to_check = [r for r in all_releases if r.created_at > cutoff_date]
    print(f"Found {len(releases_to_check)} releases within the last 30 days")

# Find CT analysis releases
ct_analysis_releases = []
for release in releases_to_check:
    if release.tag_name.startswith("ct_image_analysis-") or release.tag_name.startswith("ct_slice_analysis-"):
        release_type = "3d" if release.tag_name.startswith("ct_image_analysis-") else "2d"
        ct_analysis_releases.append((release, release_type))

if not ct_analysis_releases:
    print("No relevant CT analysis releases found.")
    exit(0)

print(f"Found {len(ct_analysis_releases)} CT analysis releases to check.")

# Create a status directory to track what we've processed
os.makedirs("data/reactions", exist_ok=True)
status_file = "data/reactions/processed_reactions.json"

# Load previously processed reactions if available
processed_reactions = {}
if os.path.exists(status_file):
    try:
        with open(status_file, 'r') as f:
            processed_reactions = json.load(f)
    except json.JSONDecodeError:
        print("Error reading status file, starting fresh")

# Track if we made any changes that need to be saved
changes_made = False

# Process each release
for release, release_type in ct_analysis_releases:
    release_id = release.id
    release_title = release.title
    release_body = release.body
    
    print(f"Processing reactions for {release_type} release: {release_title} (ID: {release_id})")
    
    # Get reactions first - if there are none, we can skip further processing
    reactions = get_release_reactions(release_id)
    if not reactions:
        print(f"No reactions found for release {release_id}, skipping...")
        continue
        
    print(f"Found {len(reactions)} reactions for release {release_id}")
    
    # Get the original MorphoSource data
    ms_tag = extract_morphosource_data(release_body)
    if not ms_tag:
        print(f"Could not extract MorphoSource tag from release: {release_title}")
        continue
    
    morphosource_data = get_morphosource_release(ms_tag)
    if not morphosource_data:
        print(f"Could not get MorphoSource data for tag: {ms_tag}")
        continue
    
    # Extract the CT analysis text
    ct_analysis = extract_ct_analysis(release_body, release_type)
    
    # Get the release status in our tracking system
    release_status = processed_reactions.get(str(release_id), {"processed_reactions": []})
    processed_reaction_ids = set(release_status["processed_reactions"])
    
    # Process the reaction data
    reaction_data = {}
    new_reactions_found = False
    
    for reaction in reactions:
        reaction_id = reaction["id"]
        
        # Skip already processed reactions unless forced
        if reaction_id in processed_reaction_ids and not specific_release:
            continue
            
        new_reactions_found = True
        changes_made = True
        content = reaction["content"]  # 👍, 👎, 😄, etc.
        user = reaction["user"]["login"]
        
        # Classify based on reaction
        is_positive = content in ["👍", "🎉", "❤️", "🚀", "😄"]
        
        # Create fine-tuning entry
        entry = create_fine_tuning_entry(morphosource_data, ct_analysis, is_positive)
        
        # Add to our reaction data
        if user not in reaction_data:
            reaction_data[user] = entry
            
        # Mark as processed
        processed_reaction_ids.add(reaction_id)
    
    # Update our tracking of processed reactions
    if new_reactions_found:
        processed_reactions[str(release_id)] = {
            "processed_reactions": list(processed_reaction_ids),
            "last_processed": datetime.now().isoformat()
        }
        
        # Save the updated reactions
        save_reaction_data(release_id, reaction_data)
        
        print(f"Processed {len(reaction_data)} reactions for release {release_id}")
    else:
        print(f"No new reactions for release {release_id}")

# Save the updated processing status only if we made changes
if changes_made:
    with open(status_file, 'w') as f:
        json.dump(processed_reactions, f, indent=2)
    print(f"Updated reaction tracking file: {status_file}")
else:
    print("No changes made, skipping status file update") 