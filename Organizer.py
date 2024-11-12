import re
from pathlib import Path

class ChapterOrganizer:
    def __init__(self, base_dir):
        # Initialize with a specific directory
        self.base_dir = Path(base_dir)  # base_dir is now an argument
        self.dirfiles = {}
        self.result = {}
        self.chpterwised = {}

    def load_files(self):
        # Traverse the directory and organize files in each subdirectory
        self.dirfiles = {
            dr.name: sorted(
                (f.name for f in dr.iterdir() if f.is_file()),
                key=lambda x: int(re.search(r'(\d+)', x).group() if re.search(r'(\d+)', x) else 0)  # Safe number extraction
            )
            for dr in self.base_dir.iterdir() if dr.is_dir()
        }

    def create_result(self):
        # Create a dictionary of file paths for each subdirectory
        self.result = {k: [f"./{self.base_dir}/{k}/{u}" for u in v] for k, v in self.dirfiles.items()}

    def extract_name_from_marks_wise(self, filepath):
        # Extract the chapter name from the Marks_Wise_Question file path
        match = re.search(r'(Ch-\d+) (.+)\.pdf', filepath)
        if match:
            chpno = match.group(1)
            chnm = match.group(2)
            return f"{chpno.capitalize()} {chnm.capitalize()}"
        return ""

    def chpterwise(self, i):
        # For a given index i, extract the files for that chapter from the result
        chp = {}
        chaptername=""
        for k, u in self.result.items():
            if i < len(u):
                chp[k] = u[i]  # Safely add the file at index i
                if 'markwise' in u[i]:
                    chaptername = self.extract_name_from_marks_wise(u[i])
            else:
                chp[k] = ""  # Return empty string if index is out of range
        chp['name'] = chaptername
        return chp

    def organize_chapters(self,n):
        # Organize the files chapter-wise
        n = n if n is not None else 15
        for i in range(n):  # Assuming there are 15 chapters
            self.chpterwised[i + 1] = self.chpterwise(i)

    def get_chapterwise_data(self):
        return self.chpterwised

    def query(self, chapter_no:int=None, category:str=None):
        # If only category is provided, return all chapters with name and filepath for that category
        if category and not chapter_no:
            result = {}
            for ch_no, data in self.chpterwised.items():
                if category in data:
                    result[ch_no] = {
                        'name': data.get('name', ''),
                        'filepath': data.get(category, '')
                    }
            return result

        # If chapter_no and category are provided, return specific chapter and category
        if chapter_no and category:
            data = self.chpterwised.get(chapter_no, {})
            if category in data:
                return {
                    'name': data.get('name', ''),
                    'filepath': data.get(category, '')
                }

        # If neither is provided, return an empty dictionary
        return {}

    def run(self,n):
        self.load_files()
        self.create_result()
        self.organize_chapters(n)

# Example usage:

