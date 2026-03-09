import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create a single supabase client instance
if SUPABASE_URL and SUPABASE_KEY:
    supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase_client = None

def upload_file_to_supabase(bucket_name: str, file_path: str, destination_name: str, content_type: str = None) -> str:
    """
    Uploads a local file to Supabase Storage and returns the public URL.
    """
    if not supabase_client:
        raise ValueError("Supabase client is not configured. Missing SUPABASE_URL or SUPABASE_KEY.")

    try:
        # Check if bucket exists, if not, you might need to handle it or assume it exists
        # Upload file
        with open(file_path, "rb") as f:
            opts = {"content-type": content_type} if content_type else {}
            supabase_client.storage.from_(bucket_name).upload(
                file=f,
                path=destination_name,
                file_options=opts
            )
        
        # Get public URL
        public_url = supabase_client.storage.from_(bucket_name).get_public_url(destination_name)
        return public_url
    except Exception as e:
        print(f"Error uploading to Supabase: {e}")
        raise e
