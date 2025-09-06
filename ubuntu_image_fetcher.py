#!/usr/bin/env python3
"""
Ubuntu Image Fetcher - A Community-Focused Image Downloading Tool
"I am because we are" - Ubuntu Philosophy

This script embodies the Ubuntu philosophy by:
- Community: Connecting to the global web community
- Respect: Handling errors gracefully and respecting servers
- Sharing: Organizing images for community use
- Practicality: Providing a useful tool for image collection
"""

import requests
import os
import time
from urllib.parse import urlparse, unquote
from pathlib import Path
import mimetypes

def print_ubuntu_banner():
    """Display the Ubuntu-inspired welcome banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                  Ubuntu Image Fetcher                        ║
║              "I am because we are"                           ║
║                                                              ║
║     A tool for mindfully collecting images from the web      ║
║              with respect and community spirit               ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def get_content_type_extension(response):
    """Extract file extension from Content-Type header"""
    content_type = response.headers.get('content-type', '')
    if 'image/' in content_type:
        extension = mimetypes.guess_extension(content_type)
        return extension if extension else '.jpg'
    return '.jpg'

def generate_filename(url, response):
    """Generate an appropriate filename from URL or content headers"""
    # First try to get filename from URL
    parsed_url = urlparse(url)
    filename = os.path.basename(unquote(parsed_url.path))
    
    # If no filename in URL, try Content-Disposition header
    if not filename or '.' not in filename:
        content_disposition = response.headers.get('content-disposition', '')
        if 'filename=' in content_disposition:
            filename = content_disposition.split('filename=')[1].strip('"\'')
        else:
            # Generate filename with timestamp and appropriate extension
            extension = get_content_type_extension(response)
            timestamp = int(time.time())
            filename = f"ubuntu_image_{timestamp}{extension}"
    
    # Ensure filename is safe for filesystem
    filename = "".join(c for c in filename if c.isalnum() or c in '.-_')
    return filename

def validate_image_response(response):
    """Validate that the response contains an image"""
    content_type = response.headers.get('content-type', '').lower()
    
    # Check if content type indicates an image
    if not content_type.startswith('image/'):
        # Also check first few bytes for image signatures
        content_start = response.content[:10]
        image_signatures = [
            b'\xff\xd8\xff',  # JPEG
            b'\x89PNG\r\n\x1a\n',  # PNG
            b'GIF87a',  # GIF87a
            b'GIF89a',  # GIF89a
            b'\x42\x4d',  # BMP
        ]
        
        if not any(content_start.startswith(sig) for sig in image_signatures):
            raise ValueError("URL does not point to a valid image file")
    
    return True

def fetch_image(url, directory="Fetched_Images"):
    """
    Fetch an image from the given URL with Ubuntu principles:
    - Community: Connect respectfully to web resources
    - Respect: Handle errors gracefully and follow web etiquette
    - Sharing: Organize for community benefit
    """
    
    print(f"🌐 Connecting to: {url}")
    print("   Approaching with Ubuntu spirit - respect and mindfulness...")
    
    # Create directory following Ubuntu principle of organization
    Path(directory).mkdir(exist_ok=True)
    print(f"📁 Ensuring community directory exists: {directory}")
    
    try:
        # Respectful headers following web etiquette
        headers = {
            'User-Agent': 'Ubuntu-Image-Fetcher/1.0 (Community Tool; Respectful Usage)',
            'Accept': 'image/*,*/*;q=0.8',
        }
        
        # Make request with timeout and respectful headers
        print("🤝 Making respectful connection...")
        response = requests.get(url, headers=headers, timeout=15, stream=True)
        response.raise_for_status()
        
        # Validate that we received an image
        validate_image_response(response)
        
        # Generate appropriate filename
        filename = generate_filename(url, response)
        filepath = Path(directory) / filename
        
        # Check file size for responsible downloading
        content_length = response.headers.get('content-length')
        if content_length and int(content_length) > 50 * 1024 * 1024:  # 50MB limit
            print("⚠️  Large file detected. Proceeding mindfully...")
        
        # Download with progress indication for larger files
        print(f"💾 Saving with Ubuntu care: {filename}")
        
        total_size = 0
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    total_size += len(chunk)
        
        # Success message with Ubuntu spirit
        size_mb = total_size / (1024 * 1024)
        print(f"✅ Successfully fetched: {filename}")
        print(f"📏 File size: {size_mb:.2f} MB")
        print(f"🎯 Image saved to: {filepath}")
        print("🌟 Connection strengthened. Community enriched.")
        
        return True, str(filepath)
        
    except requests.exceptions.Timeout:
        print("⏱️  Connection timed out - the web community is busy")
        print("   Ubuntu teaches patience. Perhaps try again later.")
        return False, "Timeout error"
        
    except requests.exceptions.ConnectionError:
        print("🌐 Unable to reach the community resource")
        print("   Ubuntu reminds us: connectivity challenges are temporary")
        return False, "Connection error"
        
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response else "Unknown"
        print(f"🚫 Server responded with status {status_code}")
        print("   Ubuntu teaches respect - the server has spoken")
        return False, f"HTTP {status_code} error"
        
    except ValueError as e:
        print(f"🖼️  Content validation failed: {e}")
        print("   Ubuntu values authenticity - this may not be an image")
        return False, str(e)
        
    except PermissionError:
        print("🔒 Permission denied saving to directory")
        print("   Ubuntu teaches: community resources need proper access")
        return False, "Permission denied"
        
    except Exception as e:
        print(f"❌ Unexpected challenge encountered: {e}")
        print("   Ubuntu philosophy: from challenges, we learn and grow")
        return False, str(e)

def main():
    """Main function embodying Ubuntu principles"""
    print_ubuntu_banner()
    
    print("Welcome, community member! 🙏")
    print("Let's mindfully gather images from our global digital community.\n")
    
    while True:
        try:
            url = input("🌍 Please enter the image URL (or 'quit' to exit): ").strip()
            
            if url.lower() in ['quit', 'exit', 'q']:
                print("\n🙏 Ubuntu blessings on your journey!")
                print("   May your digital community connections flourish.")
                break
            
            if not url:
                print("⚠️  Ubuntu teaches mindfulness - please provide a URL")
                continue
                
            # Basic URL validation
            if not url.startswith(('http://', 'https://')):
                print("🔗 Ubuntu suggests using full URLs (http:// or https://)")
                continue
            
            print("\n" + "="*60)
            success, message = fetch_image(url)
            print("="*60 + "\n")
            
            if success:
                another = input("🌟 Fetch another image? (y/n): ").strip().lower()
                if another not in ['y', 'yes']:
                    break
            else:
                retry = input("🔄 Would you like to try another URL? (y/n): ").strip().lower()
                if retry not in ['y', 'yes']:
                    break
        
        except KeyboardInterrupt:
            print("\n\n🙏 Ubuntu understanding - you wish to leave peacefully.")
            print("   Your community spirit is appreciated.")
            break
        except EOFError:
            print("\n\n👋 Peaceful departure in Ubuntu style.")
            break
    
    print("\n✨ Thank you for practicing Ubuntu digital community values!")
    print("   Your respectful approach strengthens our shared web space.")

if __name__ == "__main__":
    main()