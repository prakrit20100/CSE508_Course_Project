# CSE508_Course_Project
Building an Art History quiz game that leverages the capabilities of LLM and Information Retrieval techniques
## Installation

### Prerequisites

- [Anaconda](https://www.anaconda.com/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed
- Python 3.10

### Installation Steps

1. Clone this repository:

   ```bash
   git clone https://github.com/prakrit20100/CSE508_Course_Project.git
2. Navigate to the project directory:
   ```bash
   cd CSE508_Course_Project
3. Create a Conda environment named myenv with Python 3.10:
   ```bash
   conda create --name myenv python=3.10
4. Activate the Conda environment:
   ```bash
   conda activate myenv
5. Install the required packages:
   ```bash
   pip install -r requirements.txt
6. Download the English language model for spaCy:
   ```bash
   python -m spacy download en_core_web_sm
