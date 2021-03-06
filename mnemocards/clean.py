
import sys

sys.path.append("/usr/share/anki")
from anki import Collection

from mnemocards.utils import create_check_collection_path


QUERY = """
    select n.id
    from notes n
    left join cards c
    on c.nid = n.id
    left join (
        select did, max(n.mod) mod
        from notes n
        left join cards c
        on c.nid = n.id
        group by did
    ) d
    on d.did = c.did
    where n.mod < d.mod - 5
"""  # I use a 5 seconds margin here.


def clean(collection_path=None, profile=None):
    collection_path = create_check_collection_path(collection_path, profile)
    # Create collection.
    col = Collection(collection_path)
    # Get notes to remove.
    notes = col.db.list(QUERY)
    # Remove non-updated notes.
    print("Removing old cards with IDs:", notes)
    col.remNotes(notes)
    # Close collection.
    col.close()

