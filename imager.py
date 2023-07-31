import os
from icrawler.builtin import GoogleImageCrawler

def download_images(query, num_images=100):
    save_dir = query

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    google_crawler = GoogleImageCrawler(parser_threads=2, downloader_threads=4, storage={'root_dir': save_dir})
    google_crawler.crawl(keyword=query, max_num=num_images, file_idx_offset=0)

    # Rename the downloaded images with desired filenames
    for i, filename in enumerate(os.listdir(save_dir)):
        ext = os.path.splitext(filename)[1]  # Get the file extension (e.g., .jpg)
        new_filename = f"{query}{i:03d}{ext}"  # Format the new filename with 'spiderman' and index
        os.rename(os.path.join(save_dir, filename), os.path.join(save_dir, new_filename))

# Replace 'spiderman' with your desired search query
download_images('Spongebob', num_images= 200)
