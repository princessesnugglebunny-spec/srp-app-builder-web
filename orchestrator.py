import os
from srp_app_builder.core.cloner import RepoCloner
from srp_app_builder.core.splitter import ASTSplitter
from srp_app_builder.store.index import IndexedStore
from srp_app_builder.generator.assembler import AIAppGenerator
from srp_app_builder.generator.compiler import APKCompiler

class SRPAppBuilder:
    def __init__(self):
        self.cloner = RepoCloner()
        self.splitter = ASTSplitter()
        self.store = IndexedStore()
        self.generator = AIAppGenerator(self.store)

    def process_repository(self, repo_url):
        print(f"[*] Ingesting {repo_url}...")
        repo_path = self.cloner.clone(repo_url)
        fragments = self.splitter.analyze_and_split(repo_path)
        
        count = 0
        for frag in fragments:
            self.store.add_fragment(
                symbol_name=frag['name'],
                description=frag['description'],
                code=open(frag['path'], 'r').read(),
                dependencies=[],
                original_repo=repo_url,
                file_path=frag['path']
            )
            count += 1
        print(f"[+] Successfully indexed {count} SRP fragments.")

    def assemble_app(self, fragment_ids, description):
        return self.generator.create_app_package(fragment_ids, description)
