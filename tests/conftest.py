import tarfile

import pytest

# TODO: make customizable
REPO_TAR = 'repo.tar'

@pytest.fixture(scope='function')
def unpack_repo(tmpdir_factory: pytest.TempdirFactory) -> str:
    local = ("%s" % tmpdir_factory.mktemp("repo")).replace("\\", "/")
    with tarfile.open(REPO_TAR, 'r') as tar:
        
        import os
        
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar, local)
    return local
