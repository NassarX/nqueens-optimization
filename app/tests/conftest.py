import sys
import os

# Add the project directory to sys.path
app = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, app)
