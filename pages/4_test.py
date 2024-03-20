import streamlit as st
from annotated_text import annotated_text

st.write("testing")


annotated_text(
    "This ",
    ("is", "Verb", "#8ef"),
    " some ",
    ("annotated", "Adj", "#faa"),
    ("text", "Noun", "#afa"),
    " for those of ",
    ("you", "Pronoun", "#fea"),
    " who ",
    ("like", "Verb", "#8ef"),
    " this sort of ",
    ("thing", "Noun", "#afa"),
    ". "
    "And here's a ",
    ("word", "", "#728"),
    " with a fancy background but no label.",
)


##st.set_page_config(page_title="set page config example",page_icon="🏠")

#st.title("hi this is test st markdown")

st.markdown(
   """
<style>
.reportview-container .markdown-text-container {
    font-family: monospace;
}
.sidebar .sidebar-content {
    background-image: linear-gradient(#2e7bcf,#2e7bcf);
    color: white;
}
.Widget>label {
    color: white;
    font-family: monospace;
}
[class^="st-b"]  {
    color: white;
    font-family: monospace;
}
.st-bb {
    background-color: transparent;
}
.st-at {
    background-color: #0c0080;
}
footer {
    font-family: monospace;
}
.reportview-container .main footer, .reportview-container .main footer a {
    color: #0c0080;
}
header .decoration {
    background-image: none;
}

</style>
""",
    unsafe_allow_html=True,
)