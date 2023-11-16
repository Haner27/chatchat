import pathlib
from bs4 import BeautifulSoup
import logging
import shutil
import streamlit as st


def inject_ga():
    GA_ID = "baidu_analytics"

    GA_JS = """
<script>
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?1b9d6b726058df31cf82d9d2512d4e4e";
  var s = document.getElementsByTagName("script")[0]; 
  s.parentNode.insertBefore(hm, s);
})();
</script>
    """

    # Insert the script in the head tag of the static template inside your virtual
    index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
    print(f"editing {index_path}")
    soup = BeautifulSoup(index_path.read_text(), features="html.parser")
    if not soup.find(id=GA_ID):
        bck_index = index_path.with_suffix(".bck")
        if bck_index.exists():
            shutil.copy(bck_index, index_path)
        else:
            shutil.copy(index_path, bck_index)
        html = str(soup)
        new_html = html.replace("<head>", "<head>\n" + GA_JS)
        index_path.write_text(new_html)


inject_ga()
