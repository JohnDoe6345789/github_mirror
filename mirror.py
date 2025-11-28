#!/usr/bin/env python3
# code comments only
import argparse, os, requests
from typing import List
API="https://api.github.com"
def repo_exists(name:str, token:str)->bool:
    r=requests.get(f"{API}/user/repos",headers={"Authorization":f"token {token}"},params={"per_page":200})
    r.raise_for_status()
    return any(repo.get("name")==name for repo in r.json())
def get_repos(user:str)->List[dict]:
    r=requests.get(f"{API}/users/{user}/repos?per_page=200"); r.raise_for_status(); return r.json()
def create_repo(name:str, token:str)->None:
    r=requests.post(f"{API}/user/repos",headers={"Authorization":f"token {token}"},json={"name":name,"private":False})
    if r.status_code not in (200,201): raise RuntimeError(r.text)
def mirror_repo(src_user:str, repo:str, token:str)->None:
    os.system(f"git clone --bare https://github.com/{src_user}/{repo}.git tmp_{repo}.git")
    os.chdir(f"tmp_{repo}.git")
    os.system(f"git push --mirror https://{token}:x-oauth-basic@github.com/me/{repo}.git")
    os.chdir(".."); os.system(f"rm -rf tmp_{repo}.git")
def main():
    p=argparse.ArgumentParser(); p.add_argument("source_user"); p.add_argument("--token",default=os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"))
    a=p.parse_args()
    if not a.token: raise SystemExit("Missing GitHub token")
    for r in get_repos(a.source_user):
        n=r["name"]
        if repo_exists(n,a.token): print(f"Skip {n}"); continue
        create_repo(n,a.token); mirror_repo(a.source_user,n,a.token)
if __name__=="__main__": main()
