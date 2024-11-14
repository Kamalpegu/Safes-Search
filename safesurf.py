import streamlit as st
import utils1


def display_safe_search():
    st.title("Safe URL Checker")

    url = st.text_input("Enter a URL:", key="url_input")

    if url:
        try:
            result = utils1.get_safe_links(url)

            if isinstance(result, dict) and "error" in result:
                st.error(result["error"])
            else:
                display_results(result)


        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

def display_results(result):
  if not result:
    st.error("No results from VirusTotal.  Likely invalid input")
    return

  positives = result.get("malicious", 0)
  total_scanned = sum(result.values()) if all(isinstance(v, int) for v in result.values()) else 0
  if total_scanned == 0 :
    st.warning("No analysis data was received from VirusTotal")
    return


  st.write(f"Results: {positives} malicious / {total_scanned} scans")


if __name__ == "__main__":
    display_safe_search()