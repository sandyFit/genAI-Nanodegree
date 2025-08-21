import os
import json
import random
import chromadb
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from typing import List, Dict, Set
import re


# PromptTemplate for tailoring a property listing description to a buyer's preferences while preserving accuracy.
PERSONALIZATION_PROMPT = PromptTemplate(
    input_variables=[
        "preferences",
        "neighborhood",
        "price",
        "bedrooms",
        "bathrooms",
        "house_size",
        "description",
        "neighborhood_description"
    ],
    template="""
    Based on the user's preferences: "{preferences}"

    Please enhance this real estate listing to appeal to the user while maintaining factual accuracy:

    Neighborhood: {neighborhood}
    Price: {price}
    Bedrooms: {bedrooms}
    Bathrooms: {bathrooms}
    Size: {house_size}

    Original Description: {description}

    Neighborhood Description: {neighborhood_description}

    Create a personalized description that highlights aspects most relevant to the user's preferences.
    Keep all factual information accurate and don't add features that aren't mentioned.
    Make it compelling and tailored to their needs.
    Write in an engaging, personalized tone that connects their preferences to this property.
    """
)


class HomeMatchApp:
    """
    Main application class for generating, storing, and personalizing AI-created real estate listings.
    Handles LLM configuration, embedding setup, and ChromaDB collection initialization.
    """

    def __init__(
        self,
        api_key: str,
        api_base: str,
        *,
        expected_listings: int = 10,
        test_max_tokens: int | None = None
    ):
        """
        Initializes the HomeMatchApp with API credentials, LLM settings, and storage configuration.

        Args:
            api_key (str): OpenAI API key for authentication.
            api_base (str): Base URL for the OpenAI API endpoint.
            expected_listings (int, optional): Number of listings to generate. Defaults to 10.
            test_max_tokens (int | None, optional): Max tokens for test runs; None uses default model limits.
        """
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        if api_base:
            os.environ["OPENAI_API_BASE"] = api_base

        llm_kwargs = {"temperature": 0.8, "model_name": "gpt-3.5-turbo"}  # Increased temperature for more diversity
        if test_max_tokens:
            llm_kwargs["max_tokens"] = test_max_tokens

        self.llm = ChatOpenAI(**llm_kwargs)
        self.embeddings = OpenAIEmbeddings()

        self.chroma_client = chromadb.Client()
        self.collection_name = "real_estate_listings"

        self.listings: List[Dict] = []
        self.expected_listings = expected_listings
        
        # Track used combinations to prevent duplicates
        self.used_combinations: Set[str] = set()

        print("⚙️ HomeMatchApp initialized — no listings generated yet.")

        
        
        
        
    def _get_diverse_neighborhoods(self) -> List[str]:
        """Return a diverse list of neighborhood names"""
        
        return [
            "Downtown Lofts", "Riverside Gardens", "Oak Hill Estates", "Marina District",
            "Arts Quarter", "Historic Brownstone", "Coastal Heights", "Mountain View Villas",
            "Prairie Commons", "Tech Valley", "Suburban Oaks", "Garden District",
            "Millionaire Row", "University Heights", "Waterfront Plaza", "Sunset Ridge",
            "Heritage Square", "Innovation District", "Lakeside Commons", "Hillcrest Manor",
            "Pine Valley", "Royal Estates", "Skyline Towers", "Maple Grove",
            "Crystal Bay", "Cedar Park", "Emerald Hills", "Golden Gate Heights",
            "Silver Lake", "Copper Canyon", "Diamond District", "Platinum Shores"
        ]
    
    
    
    
    def _get_price_tiers(self) -> List[tuple]:
        """Return diverse price ranges"""
        
        return [
            (250000, 400000),   # Starter homes
            (400000, 600000),   # Mid-range family homes
            (600000, 900000),   # Premium homes
            (900000, 1400000),  # Luxury homes
            (1400000, 2200000), # High-end luxury
            (2200000, 3500000), # Ultra-luxury
            (3500000, 5000000)  # Elite estates
        ]
    
    
    
    
    def _get_property_styles(self) -> List[str]:
        """Return diverse property styles and descriptions"""
        
        return [
            "contemporary", "traditional", "modern", "colonial", "craftsman",
            "victorian", "mediterranean", "ranch", "tudor", "farmhouse",
            "industrial loft", "mid-century modern", "cape cod", "georgian",
            "spanish revival", "art deco", "minimalist", "rustic"
        ]
    
    
    
    
    def _get_description_templates(self) -> List[str]:
        """Return diverse description opening templates"""
        
        return [
            "Discover this exceptional {style} home in the heart of {neighborhood}",
            "Step into luxury with this stunning {style} residence located in {neighborhood}",
            "Experience the perfect blend of comfort and elegance in this {style} property",
            "This remarkable {style} home offers the ultimate in {neighborhood} living",
            "Nestled in the prestigious {neighborhood}, this {style} masterpiece awaits",
            "Immerse yourself in the charm of this beautifully crafted {style} home",
            "Welcome to your dream home - a spectacular {style} residence",
            "This architectural gem showcases {style} design in {neighborhood}",
            "Embrace refined living in this exquisite {style} estate",
            "Presenting a rare opportunity to own this magnificent {style} property"
        ]
        
    
    def _pick_listing_attributes(self):
        """Randomly selects and returns unique property listing attributes, including neighborhood, price, bedrooms, bathrooms, size, style, and description template, while avoiding recently used combinations.
        """  

        neighborhoods = self._get_diverse_neighborhoods()
        price_tiers = self._get_price_tiers()
        styles = self._get_property_styles()
        templates = self._get_description_templates()

        # Reset if needed
        if len(self.used_combinations) >= len(neighborhoods) * len(styles):
            self.used_combinations.clear()

        # Neighborhood choice with anti-duplication
        used_neighborhoods = {k.split('_')[0] for k in self.used_combinations}
        available = list(set(neighborhoods) - used_neighborhoods)
        neighborhood = random.choice(available or neighborhoods)

        price_min, price_max = random.choice(price_tiers)
        price = random.randint(price_min, price_max)
        price_formatted = f"${price:,}"

        bedrooms = random.choice([2, 3, 3, 4, 4, 4, 5, 5, 6])
        bathrooms = random.choice([1, 2, 2, 3, 3, 4])
        size_min = max(800, bedrooms * 400)
        size_max = min(4500, bedrooms * 800)
        size = random.randint(size_min, size_max)

        style = random.choice(styles)
        template = random.choice(templates)

        # Track uniqueness
        key = f"{neighborhood}_{style}_{bedrooms}_{bathrooms}_{size//100*100}"
        if key in self.used_combinations:
            price = max(200000, price + random.randint(-25000, 25000))
            price_formatted = f"${price:,}"
        self.used_combinations.add(key)

        return neighborhood, price, price_formatted, bedrooms, bathrooms, size, style, template

    

    def generate_single_listing(self, listing_number: int = 1) -> dict | None:
        """Generate a single diverse listing with anti-duplicate measures."""
        
        neighborhood, price, price_formatted, bedrooms, bathrooms, size, style, template = \
            self._pick_listing_attributes()

        prompt = self._build_listing_prompt(
            listing_number, neighborhood, price_formatted,
            bedrooms, bathrooms, size, style, template
        )

        text = self._call_llm(prompt)
        listing_data = self._parse_listing_json(text)

        if self._is_listing_valid(listing_data):
            return listing_data
        return None

        
    def _build_listing_prompt(self, listing_number, neighborhood, price, bedrooms, bathrooms, size, style, template):
        """Builds a structured prompt for generating a detailed, JSON-formatted real estate listing with given property attributes and template.
        """  

        
        start_phrase = template.format(style=style, neighborhood=neighborhood)
        return f"""
        Generate a detailed real estate listing #{listing_number} with these EXACT specifications:
        
        REQUIRED DETAILS:
        - Neighborhood: {neighborhood}
        - Price: {price}
        - Bedrooms: {bedrooms}
        - Bathrooms: {bathrooms}
        - Size: {size} sqft
        - Style: {style}
        
        DESCRIPTION REQUIREMENTS:
        - Start with: "{start_phrase}"
        - Make it 2-3 detailed paragraphs
        - Include specific {style} features and amenities
        - Mention outdoor spaces, kitchen details, master suite
        - Be creative with unique features that fit the style and price range
        
        NEIGHBORHOOD DESCRIPTION:
        - Write 1-2 paragraphs about {neighborhood}
        - Include amenities, schools, transportation, recreation
        - Make it feel authentic and appealing
        - Don't repeat the property description
        
        Format as valid JSON with exact keys:
        {{
            "neighborhood": "{neighborhood}",
            "price": "{price}",
            "bedrooms": {bedrooms},
            "bathrooms": {bathrooms},
            "house_size": "{size} sqft",
            "description": "your detailed property description",
            "neighborhood_description": "your neighborhood description"
        }}
        """
    
    

    def _call_llm(self, prompt: str) -> str:
        """Sends a prompt to the LLM and returns its text response, or an empty string on failure."""  
        
        try:
            response = self.llm([HumanMessage(content=prompt)])
            return getattr(response, "content", str(response)).strip()
        except Exception as e:
            print(f"❌ LLM call failed: {e}")
            return ""

    
    
    
    def _parse_listing_json(self, text: str) -> dict | None:
        """Cleans and parses a JSON-formatted string into a dictionary, returning None if parsing fails."""  
        
        text = re.sub(r"^```(?:json)?", "", text).replace("```", "").strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None
        

  
    def _is_listing_valid(self, data: dict | None) -> bool:
        """Checks if the listing data contains all required fields."""  

        if not data:
            return False
        required = ["neighborhood", "price", "bedrooms", "bathrooms", "house_size", "description", "neighborhood_description"]
        return all(k in data for k in required)



    def generate_listings(self, n: int | None = None) -> bool:
        """Generate n diverse listings and store in self.listings, no embeddings."""
        
        n = n or self.expected_listings
        print(f"🛠 Generating {n} diverse listings...")
        
        # Clear used combinations for fresh generation
        self.used_combinations.clear()
        
        listings: List[Dict] = []
        failed_attempts = 0
        max_failures = 5
        
        for i in range(1, n + 1):
            print(f"  Generating listing {i}/{n}...")
            item = self.generate_single_listing(i)
            
            if item and isinstance(item, dict):
                listings.append(item)
                failed_attempts = 0  # Reset failure counter on success
            else:
                failed_attempts += 1
                print(f"  ⚠️ Generation failed for listing #{i}")
                
                if failed_attempts >= max_failures:
                    print(f"❌ Too many failures ({max_failures}). Stopping generation.")
                    break
                    
                # Continue trying with next listing number
                continue
        
        self.listings = listings
        success_rate = len(self.listings) / n * 100
        print(f"✅ Generated {len(self.listings)} listings ({success_rate:.1f}% success rate).")
        
        if self.listings:
            self._analyze_diversity()
            return True
        else:
            return False
        
        
        

    def _analyze_diversity(self):
        """Analyze and report on the diversity of generated listings"""
        if not self.listings:
            return
        
        neighborhoods = [l['neighborhood'] for l in self.listings]
        prices = [l['price'] for l in self.listings]
        bedrooms = [l['bedrooms'] for l in self.listings]
        
        unique_neighborhoods = len(set(neighborhoods))
        unique_prices = len(set(prices))
        unique_bedrooms = len(set(bedrooms))
        
        print(f"📊 Diversity Analysis:")
        print(f"  🏘️  Neighborhoods: {unique_neighborhoods}/{len(neighborhoods)} unique")
        print(f"  💰 Prices: {unique_prices}/{len(prices)} unique")  
        print(f"  🛏️  Bedroom counts: {unique_bedrooms} different configurations")
        
        # Warn about duplicates
        neighborhood_counts = {}
        for n in neighborhoods:
            neighborhood_counts[n] = neighborhood_counts.get(n, 0) + 1
        
        duplicates = {n: count for n, count in neighborhood_counts.items() if count > 1}
        if duplicates:
            print(f"  ⚠️  Duplicate neighborhoods found: {duplicates}")
        else:
            print(f"  ✅ No duplicate neighborhoods!")
            
            
                                 

    def save_listings(self, filepath: str = "listings.json"):
        """Save current listings to a JSON file."""
        
        with open(filepath, "w") as f:
            json.dump(self.listings, f, indent=2)
        print(f"💾 Listings saved to {filepath}")
        
        
        

    def load_listings(self, filepath: str = "listings.json"):
        """Load listings from JSON and rebuild embeddings."""
        
        with open(filepath) as f:
            self.listings = json.load(f)
        print(f"📂 Loaded {len(self.listings)} listings from {filepath}")
        self.setup_vector_database()
        
        
        

    def build_embeddings_from_current_listings(self):
        """Create vector DB from whatever is in self.listings."""
        if not self.listings:
            print("❌ No listings loaded — cannot build embeddings.")
            return
        self.setup_vector_database()
        
        
        

    def setup_vector_database(self):
        """Set up ChromaDB vector database with embeddings."""
        
        try:
            try:
                self.chroma_client.delete_collection(self.collection_name)
            except:
                pass

            collection = self.chroma_client.create_collection(self.collection_name)

            documents = []
            metadatas = []
            ids = []

            for i, listing in enumerate(self.listings):
                full_text = f"""Neighborhood: {listing['neighborhood']}
                Price: {listing['price']}
                Bedrooms: {listing['bedrooms']}
                Bathrooms: {listing['bathrooms']}
                Size: {listing['house_size']}
                Description: {listing['description']}
                Neighborhood Description: {listing['neighborhood_description']}"""
                documents.append(full_text.strip())
                metadatas.append(listing)
                ids.append(f"listing_{i}")

            collection.add(documents=documents, metadatas=metadatas, ids=ids)
            print(f"✅ Successfully added {len(documents)} listings to vector database.")
        except Exception as e:
            print(f"❌ Error setting up vector database: {e}")
            raise
            
            
            

    def search_listings(self, user_preferences: str, num_results: int = 5) -> List[Dict]:
        """Search for listings based on user preferences."""
        
        try:
            collection = self.chroma_client.get_collection(self.collection_name)
            if not self.listings:
                print("❌ No listings loaded — cannot search.")
                return []

            # Ensure at least 1 result
            safe_n_results = max(1, min(num_results, len(self.listings)))

            results = collection.query(
                query_texts=[user_preferences],
                n_results=safe_n_results
            )

            matching_listings = []
            if results['metadatas'] and results['metadatas'][0]:
                matching_listings.extend(results['metadatas'][0])
            return matching_listings
        except Exception as e:
            print(f"❌ Error searching listings: {e}")
            return []
    
    

    def extract_budget(self, query: str) -> int | None:
        """Robust budget extraction supporting: $1,800,000, 1,800,000, 1.8M, 500k, 500, 'under 500' (→ 500k heuristic)."""
        
        import re
        if not query:
            return None
        q = str(query)
        ql = q.lower()

        # $ followed by numbers, optional decimal, optional k/m suffix
        m = re.search(r'\$\s*([\d,]+(?:\.\d+)?)\s*([km]?)\b', ql)
        if m:
            num_str = m.group(1).replace(',', '')
            suffix = m.group(2)
            try:
                val = float(num_str)
            except:
                return None
            if suffix == 'k':
                val *= 1_000
            elif suffix == 'm':
                val *= 1_000_000
            return int(val)

        # plain number with commas (e.g. 1,800,000)
        m = re.search(r'\b(\d{1,3}(?:,\d{3})+)\b', q)
        if m:
            return int(m.group(1).replace(',', ''))

        # number with suffix like 500k or 1.8m (no $)
        m = re.search(r'\b(\d+(?:\.\d+)?)\s*([km])\b', ql)
        if m:
            val = float(m.group(1))
            if m.group(2) == 'k':
                val *= 1_000
            else:
                val *= 1_000_000
            return int(val)

        # contextual short numbers (e.g. "under 500" -> 500k)
        m = re.search(r'(?:budget|under|max|up to|<=|less than)\s*\$?\s*(\d{2,4})\b', ql)
        if m:
            num = int(m.group(1))
            if num < 5000:
                return int(num * 1000)
            return num

        # fallback: standalone 3-4 digit -> treat as thousands when < 5000
        m = re.search(r'\b(\d{3,4})\b', ql)
        if m:
            num = int(m.group(1))
            return int(num * 1000) if num < 5000 else num

        return None
    
    
    def extract_bedrooms(self, query: str) -> int | None:
        if not query: return None
        ql = query.lower()
        m = re.search(r'(\d+)\s*(?:-?bedroom|bedrooms|beds|bed)\b', ql)
        if m: return int(m.group(1))
        return None


    

    def simple_filter_listings(self, budget: int = None, min_bedrooms: int = None) -> List[Dict]:
        """Filter listings by basic constraints"""
        filtered = []

        for listing in self.listings:
            # Parse price
            try:
                price_str = listing['price'].replace('$', '').replace(',', '')
                price = int(price_str)
            except:
                continue

            # Check budget constraint
            if budget and price > budget:
                continue

            # Check bedroom constraint  
            if min_bedrooms and listing['bedrooms'] < min_bedrooms:
                continue

            filtered.append(listing)

        return filtered
    

    

    def improved_search_listings(self, user_preferences, num_results=5):
        """
        Searches for listings based on user preferences, using vector search + 
        constraint filtering for budget and bedrooms.
        """
        print(f"\n🔍 SEARCHING FOR: '{user_preferences}'")
        print("=" * 80)

        # Step 1: Process preferences into a structured query
        processed_query = self.process_preferences(user_preferences)
        print("📝 Step 1: Processing preferences...")
        print(f"   Result: {processed_query}\n")

        # Step 2: Extract constraints
        budget = self.extract_budget(user_preferences)
        min_bedrooms = self.extract_bedrooms(user_preferences)
        budget_text = f"${budget:,}" if budget else "None"
        print("🔎 Step 2: Searching vector database...")
        print(f"🔍 Detected constraints: Budget={budget_text}, Min bedrooms={min_bedrooms}")

        # Step 3: Vector search using your existing method
        vector_results = self.search_listings(user_preferences, num_results=len(self.listings))

        # Step 4: Apply filtering to vector results
        def filter_vector_results(results, budget=None, min_bedrooms=None):
            filtered = []
            for r in results:
                try:
                    price = int(r["price"].replace("$", "").replace(",", ""))
                except:
                    continue
                if budget and price > budget:
                    continue
                if min_bedrooms and r.get("bedrooms", 0) < min_bedrooms:
                    continue
                filtered.append(r)
            return filtered

        filtered_results = filter_vector_results(vector_results, budget, min_bedrooms)
        print(f"📋 {len(filtered_results)}/{len(self.listings)} properties match constraints")

        if not filtered_results:
            print("❌ No matching properties found\n")
            print("💡 Try:")
            print("   - Different keywords")
            print("   - Broader criteria")
            print("   - Check if listings are loaded")
            return []

        # Step 5: Limit results to requested number
        results_to_show = filtered_results[:num_results]
        print(f"✅ Found {len(results_to_show)} matching properties\n")

        # Step 6: Display results
        for i, r in enumerate(results_to_show, start=1):
            print(f"🏠 PROPERTY {i}")
            print(f"   📍 Location: {r['neighborhood']}")
            print(f"   💰 Price: {r['price']}")
            print(f"   🛏️  Specs: {r['bedrooms']} bed, {r['bathrooms']} bath, {r['house_size']} sqft")
            desc_preview = r.get('description', '')
            if len(desc_preview) > 80:
                desc_preview = desc_preview[:77] + "..."
            print(f"   📄 Preview: {desc_preview}\n")

        return results_to_show


        

    def personalize_description(self, listing: Dict, user_preferences: str) -> str:
        """Generates a personalized property description based on user preferences and listing details."""  

        try:
            formatted_prompt = PERSONALIZATION_PROMPT.format(
                preferences=user_preferences,
                neighborhood=listing["neighborhood"],
                price=listing["price"],
                bedrooms=listing["bedrooms"],
                bathrooms=listing["bathrooms"],
                house_size=listing["house_size"],
                description=listing["description"],
                neighborhood_description=listing["neighborhood_description"]
            )
            response = self.llm([HumanMessage(content=formatted_prompt)])
            return response.content.strip()
        except Exception as e:
            print(f"❌ Error personalizing description: {e}")
            return listing.get("description", "")       
        
        

    def process_preferences(self, preferences: str) -> str:
        """Process and format user preferences for better searching."""
        
        processing_prompt = PromptTemplate(
            input_variables=["preferences"],
            template="""
            Convert these user preferences into a well-structured search query for real estate:
            
            User Input: "{preferences}"
            
            Extract and emphasize key requirements like:
            - Number of bedrooms/bathrooms
            - Price range or budget constraints
            - Location preferences (neighborhood type, proximity needs)
            - Specific amenities (pool, garage, garden, etc.)
            - Lifestyle preferences (family-friendly, urban, suburban)
            - Transportation needs
            - Special requirements (accessibility, pet-friendly, etc.)
            
            Create a comprehensive search description that captures both explicit and implicit needs.
            Focus on the most important criteria mentioned.
            
            Format: "Search Query: [your optimized search text]"
            """
        )
        try:
            formatted_prompt = processing_prompt.format(preferences=preferences)
            response = self.llm([HumanMessage(content=formatted_prompt)])
            return response.content.strip()
        except Exception as e:
            print(f"❌ Error processing preferences: {e}")
            return f"Search Query: {preferences}"

        
        
        
    def get_quality_report(self) -> Dict:
        """Generate a comprehensive quality report of current listings"""
        if not self.listings:
            return {"error": "No listings to analyze"}
        
        neighborhoods = [l['neighborhood'] for l in self.listings]
        prices = [l['price'] for l in self.listings]
        bedrooms = [l['bedrooms'] for l in self.listings]
        bathrooms = [l['bathrooms'] for l in self.listings]
        
        # Count duplicates
        neighborhood_counts = {}
        price_counts = {}
        
        for item in neighborhoods:
            neighborhood_counts[item] = neighborhood_counts.get(item, 0) + 1
        for item in prices:
            price_counts[item] = price_counts.get(item, 0) + 1
            
        duplicates = {
            "neighborhoods": {k: v for k, v in neighborhood_counts.items() if v > 1},
            "prices": {k: v for k, v in price_counts.items() if v > 1}
        }
        
        diversity_score = (
            len(set(neighborhoods)) / len(neighborhoods) * 40 +
            len(set(prices)) / len(prices) * 40 +
            min(len(set(bedrooms)), 4) / 4 * 20
        )
        
        return {
            "total_listings": len(self.listings),
            "unique_neighborhoods": len(set(neighborhoods)),
            "unique_prices": len(set(prices)),
            "bedroom_range": f"{min(bedrooms)}-{max(bedrooms)}",
            "bathroom_range": f"{min(bathrooms)}-{max(bathrooms)}",
            "duplicates": duplicates,
            "diversity_score": round(diversity_score, 1),
            "quality_grade": "A" if diversity_score >= 90 else "B" if diversity_score >= 75 else "C" if diversity_score >= 60 else "D"
        }
    