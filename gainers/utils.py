import os


def contained_suffixes(suffixes, directory):
    """Removes suffixes that no file in directory ends with"""
    contained = set(
        os.path.splitext(item)[-1]
        for item
        in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, item))
    )
    return (suffix for suffix in suffixes if suffix in contained)
