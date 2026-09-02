from veracode_api_py import Applications, Teams
import time

def get_application(app_name, attempt=1):
    try:
        applications = Applications().get_by_name(app_name)
        for app in applications:
            if app['profile']["name"].lower().strip() == app_name.lower().strip():
                return app
        print(f"No application found with name: {app_name}")
        return None
    except Exception as e:
        if attempt < 5:
            print(f"Attempt {attempt} failed: {e}")
            time.sleep(2 ** attempt)  # Exponential backoff
            return get_application(app_name, attempt + 1)
        else:
            print(f"Failed to fetch application after {attempt} attempts: {e}")
            return None

def try_get_team_by_name(team_name, attempt=1):
    try:
        teams = Teams().get_by_name(team_name)
        for team in teams:
            if team['team_name'].lower().strip() == team_name.lower().strip():
                return team["team_id"]
        print(f"No team found with name: {team_name}")
        return None
    except Exception as e:
        if attempt < 5:
            print(f"Attempt {attempt} failed: {e}")
            time.sleep(2 ** attempt)  # Exponential backoff
            return try_get_team_by_name(team_name, attempt + 1)
        else:
            print(f"Failed to fetch team after {attempt} attempts: {e}")
            return None

def main():
    name_of_team_to_archive = input("Enter the name of the team to use to archive applications: ").strip()
    archived_team_id = try_get_team_by_name(name_of_team_to_archive)
    if not archived_team_id:
        print(f"Team '{name_of_team_to_archive}' not found. Please ensure the team exists before running this script.")
        return -1

    with open('applications.txt', 'r') as f:
        application_names = [line.strip() for line in f if line.strip()]

    successes = []
    failures = []
    for app_name in application_names:
        application = get_application(app_name)
        if application:
            app_id = application['guid']
            business_criticality = application['profile']['business_criticality']
            description = application['profile'].get('description', None)
            teams = [archived_team_id]  # Move to archived team
            policies = application['profile'].get('policies', [])
            policy_guid = policies[0]['guid'] if policies else None
            custom_fields = application['profile'].get('custom_fields', [])
            business_owners = application['profile'].get('business_owners', [])
            bus_owner_name = business_owners[0].get('name', None) if business_owners else None
            bus_owner_email = business_owners[0].get('email', None) if business_owners else None
            git_repo_url = application['profile'].get('git_repo_url', None)
            tags = application['profile'].get('tags', '')
            business_unit_id = application['profile']['business_unit']['guid'] if application['profile'].get('business_unit') else None
            
            try:
                Applications().update(
                    guid=app_id,
                    app_name=app_name,
                    business_criticality=business_criticality,
                    description=description,
                    business_unit=business_unit_id,
                    teams=teams,
                    policy_guid=policy_guid,
                    custom_fields=custom_fields,
                    bus_owner_name=bus_owner_name,
                    bus_owner_email=bus_owner_email,
                    git_repo_url=git_repo_url,
                    tags=tags
                )
                print(f"    Updated: {app_name}")
                successes.append(app_name)
            except Exception as e:
                print(f"    Error updating {app_name}: {e}")
                failures.append(app_name)
                time.sleep(10)  # brief pause before next operation
        else:
            print(f"Skipping archiving for {app_name} as it was not found.")

    print("\nSummary:")
    print(f"Successfully archived applications: {len(successes)}")
    for app in successes:
        print(f"  - {app}")
    print(f"Failed to archive applications: {len(failures)}")
    for app in failures:
        print(f"  - {app}")

if __name__ == "__main__":
    main()
