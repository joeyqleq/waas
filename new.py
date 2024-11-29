import os
import re

# Define the old Matomo tracking code pattern
old_matomo_pattern = r'<!-- Matomo -->.*?<!-- End Matomo Code -->'

# Define the new Matomo tracking code to insert
new_matomo_code = """
<!-- Matomo -->
<script>
  var _paq = window._paq = window._paq || [];
  /* tracker methods like "setCustomDimension" should be called before "trackPageView" */
  _paq.push(["setDocumentTitle", document.domain + "/" + document.title]);
  _paq.push(["setCookieDomain", "*.savedbywaas.tech"]);
  _paq.push(["setDomains", ["*.savedbywaas.tech","*.www.savedbywaas.tech","*.savedbywaas.tech","*.www.savedbywaas.tech"]]);
  _paq.push(["enableCrossDomainLinking"]);
  _paq.push(['trackPageView']);
  _paq.push(['enableLinkTracking']);
  (function() {
    var u="https://matomo.joeyq.tech/";
    _paq.push(['setTrackerUrl', u+'matomo.php']);
    _paq.push(['setSiteId', '6']);
    var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
    g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
  })();
</script>
<noscript><p><img referrerpolicy="no-referrer-when-downgrade" src="https://matomo.joeyq.tech/matomo.php?idsite=6&amp;rec=1" style="border:0;" alt="" /></p></noscript>
<!-- End Matomo Code -->
"""

# Function to process each HTML file
def process_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove old Matomo code if exists
    content = re.sub(old_matomo_pattern, '', content, flags=re.DOTALL)

    # Insert new Matomo code before </head>
    if '</head>' in content:
        content = content.replace('</head>', new_matomo_code + '</head>', 1)

        # Write the modified content back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {file_path}")
    else:
        print(f"Skipping (no </head> tag found): {file_path}")

# Function to recursively search for HTML files in the current folder and subdirectories
def search_and_process_html_files(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.html'):
                file_path = os.path.join(dirpath, filename)
                process_html_file(file_path)

# Run the script on the current directory
if __name__ == '__main__':
    search_and_process_html_files(os.getcwd())