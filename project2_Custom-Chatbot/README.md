# 🌱 CompostPal: NYC Composting Assistant

Your friendly NYC composting chatbot that helps residents find compost drop-off locations across all five boroughs using real-time 2025 data.

## 🗽 Project Overview

**CompostPal** is a custom chatbot powered by OpenAI embeddings and NYC's open data that solves a real urban sustainability challenge. While composting at home can be difficult in dense cities like New York, this tool makes it easy for residents to find nearby compost drop-off locations, supporting the city's zero-waste goals.

### The Problem
- Most NYC residents live in small apartments without outdoor space for composting
- Finding current, accurate information about compost drop-off sites is challenging  
- Generic AI models lack up-to-date, location-specific data about NYC's composting infrastructure

### The Solution
CompostPal uses semantic search on a curated 2025 dataset of NYC compost drop-off locations to provide:
- ✅ Immediate, actionable location information
- ✅ Current hours and accessibility details
- ✅ Site-specific restrictions (e.g., meat/dairy policies)
- ✅ Borough and neighborhood-level precision

## 📊 Dataset

**Source**: `Food_Scrap_Drop-Off_Locations_in_NYC2025.csv` from NYC Open Data Portal

**Key Features**:
- 591 original locations across all 5 NYC boroughs
- Cleaned to 201 locations with complete address information
- Sampled to 20 representative sites (4 per borough) for demonstration
- Includes site names, addresses, hours, hosting organizations, and special notes

**Data Processing**:
- Removed entries missing address information
- Standardized notes using custom summarization function
- Created structured text entries combining all relevant fields
- Generated embeddings using OpenAI's `text-embedding-ada-002` model

## 🚀 Features

### Core Functionality
- **Semantic Search**: Uses OpenAI embeddings to find most relevant locations based on user queries
- **Token Management**: Intelligent prompt composition that stays within API limits
- **Interactive Mode**: Continuous conversation interface with helpful commands
- **Comparison Mode**: Side-by-side comparison with baseline GPT responses

### Smart Data Processing
- **Borough-based filtering**: Find locations by specific NYC borough
- **Hours extraction**: Get operating hours and schedules
- **Restriction handling**: Identifies sites with special material restrictions
- **Neighborhood precision**: Leverages NYC's Neighborhood Tabulation Area (NTA) data

## 🛠️ Installation & Setup

### Prerequisites
```bash
pip install pandas openai tiktoken scipy
```

### API Setup
1. Obtain an OpenAI API key
2. Replace `<YOUR API KEY>` in the notebook with your actual key:
```python
openai.api_key = "your-api-key-here"
```

### Data Files
- Place `Food_Scrap_Drop-Off_Locations_in_NYC2025.csv` in the `data/` directory
- The notebook will generate `compostpal_embeddings.csv` for reuse

## 📝 Usage

### Basic Query
```python
# Load the processed data
df = load_embeddings_from_csv()

# Ask a question
question = "Where can I compost in Brooklyn?"
answer = answer_question(question, df)
print(answer)
```

### Interactive Mode
```python
# Start the interactive chatbot
start_compostpal()
```

### Example Questions
- "Where can I compost in Brooklyn?"
- "What are the composting hours in Manhattan?"
- "Which sites accept meat and dairy?"
- "Show me weekend compost drop-off locations"
- "Are there any 24/7 compost sites?"

## 📈 Performance Comparison

CompostPal significantly outperforms baseline GPT responses:

| Aspect | Baseline GPT | CompostPal |
|--------|--------------|------------|
| **Actionability** | Generic advice requiring research | Specific addresses and hours |
| **Currency** | Potentially outdated information | Current 2025 NYC data |
| **Precision** | Broad generalizations | Targeted, location-specific results |
| **User Experience** | Requires follow-up research | Complete information upfront |

### Example Comparison

**Question**: "Where can I compost in Brooklyn?"

**Baseline Answer**: 
> "There are several places to compost in Brooklyn including community gardens, local farms, and compost drop-off locations... It is recommended to contact the specific location beforehand..."

**CompostPal Answer**:
> "📍 Rogers / Tilden / Veronica Place Garden  
> Address: 2601 - 2603 Tilden Avenue, Brooklyn 11226  
> Neighborhood: East Flatbush-Erasmus  
> Hours: Saturday (Start Time: 10:00 AM - End Time: 12:00 PM)"

## 🏗️ Technical Architecture

### Data Pipeline
1. **Data Cleaning**: Remove incomplete entries, standardize format
2. **Text Processing**: Combine multiple fields into searchable text
3. **Embedding Generation**: Convert text to numerical vectors using OpenAI
4. **Semantic Search**: Find relevant entries using cosine similarity
5. **Response Generation**: Compose context-aware prompts for completion

### Key Functions
- `build_text()`: Formats location data into structured text entries
- `summarize_note()`: Extracts key information from site notes
- `get_rows_sorted_by_relevance()`: Semantic search implementation
- `create_prompt()`: Context-aware prompt composition with token management
- `answer_question()`: Main query processing function

## 📋 Requirements

- Python 3.7+
- OpenAI API access
- Required packages: pandas, openai, tiktoken, scipy
- NYC Open Data: Food Scrap Drop-Off Locations dataset

## 🔧 Configuration

### Model Settings
- **Embedding Model**: `text-embedding-ada-002`
- **Completion Model**: `gpt-3.5-turbo-instruct`
- **Max Prompt Tokens**: 1,800
- **Max Answer Tokens**: 150

### Customization Options
- Adjust `max_prompt_tokens` for longer context
- Modify `top_k` in search function for more/fewer results
- Update `summarize_note()` function for different note processing

## 🌟 Key Insights

### Why This Dataset Works
- **Fills Knowledge Gaps**: GPT models lack current NYC composting data
- **Hyperlocal Precision**: Street-level addresses and neighborhood details
- **Dynamic Information**: Captures frequently changing hours and policies
- **Real-world Constraints**: Includes practical details like material restrictions

### Semantic Search Benefits
- Handles natural language queries (not just keyword matching)
- Understands context and intent beyond exact word matches
- Automatically prioritizes most relevant information
- Scales efficiently with larger datasets

## 🤝 Contributing

To extend CompostPal:
1. Update the dataset with more recent NYC open data
2. Add more boroughs or expand to other cities
3. Implement additional filtering (wheelchair accessibility, specific materials)
4. Add location-based features using coordinate data

## 📄 License

This project uses NYC Open Data, which is publicly available. Please respect OpenAI's API and Udacity's terms of service when using the embedding and completion services.

## 🙏 Acknowledgments

- NYC Open Data Portal for providing current composting location data
- OpenAI for embedding and completion API services
- The NYC zero-waste community for inspiring sustainable urban solutions

---

*Making composting accessible in the city that never sleeps* 🌱🗽
