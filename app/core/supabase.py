import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
# Use SERVICE_ROLE_KEY or SECRET_KEY for backend (preferring these over anon key for uploads)
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_ANON_KEY")

# Create a single supabase client instance
if SUPABASE_URL and SUPABASE_KEY:
    supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase_client = None

def upload_file_to_supabase(bucket_name: str, file_path: str, destination_name: str, content_type: str = None) -> str:
    """
    Uploads a local file to Supabase Storage and returns the public URL.
    Attempts to create the bucket if it doesn't exist.
    """
    if not supabase_client:
        raise ValueError("Supabase client is not configured. Missing SUPABASE_URL or SUPABASE_KEY.")

    try:
        # Ensure bucket exists
        try:
            supabase_client.storage.get_bucket(bucket_name)
        except Exception:
            # If get_bucket fails, attempt to create it as a public bucket
            try:
                supabase_client.storage.create_bucket(bucket_name, options={"public": True})
                print(f"Created missing public bucket: {bucket_name}")
            except Exception as create_err:
                print(f"Failed to create bucket {bucket_name}: {create_err}")
                # We continue anyway, as the upload might still work if it was just a transient error

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
