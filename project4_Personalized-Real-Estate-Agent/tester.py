import ipywidgets as widgets
from IPython.display import display, clear_output


class SimpleHomeMatchTester:
    """Interactive widget for testing HomeMatch search and personalization functionality"""
    
    def __init__(self, app):
        """
        Initialize the tester with a HomeMatchApp instance
        
        Args:
            app: Your initialized HomeMatchApp instance with loaded listings
        """
        self.app = app
        self.last_results = []
        self.create_widgets()
    
    def create_widgets(self):
        """Create and configure all UI widgets"""
        
        # Header
        self.title = widgets.HTML(
            value="<h3>🏠 HomeMatch Functionality Tester</h3>"
            "<p style='color: #666;'>Test search and personalization features</p>"
        )
        
        # Main query input
        self.query = widgets.Textarea(
            value="I want a family home with 4 bedrooms and a backyard under $800,000",
            placeholder="Describe what you're looking for...",
            description="Search Query:",
            style={'description_width': '100px'},
            layout=widgets.Layout(width='95%', height='80px'),
            rows=3
        )
        
        # Controls row
        self.num_results = widgets.IntSlider(
            value=2,
            min=1,
            max=5,
            description="Max Results:",
            style={'description_width': '100px'},
            layout=widgets.Layout(width='300px')
        )
        
        # Action buttons
        self.search_btn = widgets.Button(
            description="🔍 Search",
            button_style='primary',
            tooltip="Search for matching properties",
            layout=widgets.Layout(width='120px', margin='0 5px 0 0')
        )
        
        self.personalize_btn = widgets.Button(
            description="✨ Personalize",
            button_style='success',
            tooltip="Generate personalized descriptions",
            layout=widgets.Layout(width='140px', margin='0 5px 0 0')
        )
        
        self.clear_btn = widgets.Button(
            description="🧹 Clear",
            button_style='',
            tooltip="Clear output area",
            layout=widgets.Layout(width='100px', margin='0 5px 0 0')
        )
        
        # Output area with improved scrolling and sizing
        self.output = widgets.Output(
            layout=widgets.Layout(
                height='600px',  # Increased height
                width='100%',
                overflow='auto',  # Changed to 'auto' instead of 'overflow_y'
                border='2px solid #ddd',
                padding='15px',
                margin='10px 0',
                background_color='#fafafa'
            )
        )
        
        # Connect button actions
        self.search_btn.on_click(self._handle_search)
        self.personalize_btn.on_click(self._handle_personalize)
        self.clear_btn.on_click(self._handle_clear)
        
        # Initialize output with welcome message
        with self.output:
            print("🧹 Output area ready - enter a query and click Search to begin!")
            
            
    
    def _handle_search(self, button):
        """Handle search button click"""
        with self.output:
            clear_output(wait=True)  # Clear previous output
            
            query = self.query.value.strip()
            if not query:
                print("❌ Please enter a search query")
                return
            
            print(f"🔍 SEARCHING FOR: '{query}'")
            print("=" * 80)
            
            try:
                # Step 1: Process preferences
                print("📝 Step 1: Processing preferences...")
                processed_query = self.app.process_preferences(query)
                print(f"   Result: {processed_query}")
                print()
                
                # Step 2: Search listings
                print("🔎 Step 2: Searching vector database...")
                results = self.app.improved_search_listings(processed_query, num_results=self.num_results.value)

                if not results:
                    print("❌ No matching properties found")
                    print()
                    print("💡 Try:")
                    print("   - Different keywords")
                    print("   - Broader criteria")
                    print("   - Check if listings are loaded")
                    return
                
                # Step 3: Display results
                print(f"✅ Found {len(results)} matching properties")
                print()
                self.last_results = results
                
                for i, prop in enumerate(results, 1):
                    self._display_property_summary(i, prop)
                
                print("💡 Click '✨ Personalize' to see customized descriptions!")
                print("=" * 80)
                
            except Exception as e:
                print(f"❌ Error during search: {str(e)}")
                print("💡 Make sure your HomeMatchApp is properly initialized")
                
                
    
    def _handle_personalize(self, button):
        """Handle personalize button click"""
        with self.output:
            clear_output(wait=True)  # Clear previous output
            
            if not self.last_results:
                print("❌ No search results available")
                print("💡 Run a search first, then click personalize")
                return
            
            query = self.query.value.strip()
            print(f"✨ PERSONALIZED DESCRIPTIONS FOR: '{query}'")
            print("=" * 80)
            
            try:
                for i, prop in enumerate(self.last_results, 1):
                    print(f"\n🏠 PROPERTY {i} - PERSONALIZED VIEW")
                    print(f"📍 {prop['neighborhood']} | {prop['price']} | {prop['bedrooms']}bed/{prop['bathrooms']}bath")
                    print("-" * 60)
                    
                    # Generate personalized description
                    print("🔄 Generating personalized description...")
                    print()
                    personalized = self.app.personalize_description(prop, query)
                    print(personalized)
                    print("\n" + "=" * 80)
                    
            except Exception as e:
                print(f"❌ Error during personalization: {str(e)}")
                
                
    
    def _handle_clear(self, button):
        """Handle clear button click"""
        with self.output:
            clear_output(wait=True)
            print("🧹 Output cleared - ready for new tests!")
            print("💡 Enter a query and click Search to begin")
        self.last_results = []
        
        
    
    def _display_property_summary(self, index, prop):
        """Display a concise property summary"""
        print(f"🏠 PROPERTY {index}")
        print(f"   📍 Location: {prop['neighborhood']}")
        print(f"   💰 Price: {prop['price']}")
        print(f"   🛏️  Specs: {prop['bedrooms']} bed, {prop['bathrooms']} bath, {prop['house_size']}")
        print(f"   📄 Preview: {prop['description'][:100]}...")
        print()
    
    
    
    
    def display(self):
        """Display the complete widget interface"""
        
        # Controls section
        controls_row = widgets.HBox([
            self.num_results
        ], layout=widgets.Layout(justify_content='flex-start', margin='0 0 10px 0'))
        
        # Button controls
        button_controls = widgets.HBox([
            self.search_btn,
            self.personalize_btn, 
            self.clear_btn
        ], layout=widgets.Layout(justify_content='flex-start', margin='0 0 10px 0'))
        
        # Output section header
        output_header = widgets.HTML(
            value="<h4>📋 Output:</h4><p style='color: #666; margin: 0;'>Results will appear in the scrollable area below</p>",
            layout=widgets.Layout(margin='10px 0 5px 0')
        )
        
        # Main interface layout with better spacing
        interface = widgets.VBox([
            self.title,
            widgets.HTML("<hr style='margin: 10px 0;'>"),
            self.query,
            controls_row,
            button_controls,
            output_header,
            self.output
        ], layout=widgets.Layout(width='100%', padding='10px'))
        
        display(interface)

        

class QuickExamples:
    """Provides quick example queries for testing"""
    
    EXAMPLES = [
        "Budget starter home under $400k with good schools nearby",
        "Family house with large backyard and 3+ bedrooms within $500k",
        "Pet-friendly house with 2 bedrooms fenced yard and dog park access",
        "Investment property with rental potential under $600k"
    ]
    
    
    @classmethod
    def create_widget(cls, tester):
        """Create example buttons that populate the tester's query field"""
        
        buttons = []
        for i, example in enumerate(cls.EXAMPLES):
            # Create short label for button
            label = example[:35] + "..." if len(example) > 35 else example
            
            btn = widgets.Button(
                description=label,
                tooltip=example,  # Show full text on hover
                layout=widgets.Layout(
                    width='280px', 
                    height='35px',
                    margin='2px'
                ),
                button_style='info'
            )
            
            # Create handler that sets the query
            def make_handler(query_text):
                def handler(b):
                    tester.query.value = query_text
                    # Clear output when new example is selected
                    with tester.output:
                        clear_output(wait=True)
                        print(f"📝 Query set to: {query_text}")
                        print("💡 Click '🔍 Search' to find matching properties")
                return handler
            
            btn.on_click(make_handler(example))
            buttons.append(btn)
        
        # Arrange in rows of 2 for better layout
        rows = []
        for i in range(0, len(buttons), 2):
            row_buttons = buttons[i:i+2]
            row = widgets.HBox(
                row_buttons, 
                layout=widgets.Layout(justify_content='flex-start')
            )
            rows.append(row)
        
        return widgets.VBox([
            widgets.HTML("<h4>📋 Quick Test Examples</h4>"),
            widgets.HTML("<p style='color: #666;'>Click any example to populate the search field</p>"),
            widgets.VBox(rows, layout=widgets.Layout(margin='10px 0'))
        ], layout=widgets.Layout(margin='0 0 20px 0'))
    


def create_simple_tester(app):
    """
    Create and display the complete HomeMatch testing interface
    
    Args:
        app: Initialized HomeMatchApp instance with loaded listings
        
    Returns:
        SimpleHomeMatchTester: The tester instance for programmatic access
        
    Example:
        from services import HomeMatchApp
        from tester import create_simple_tester
        
        app = HomeMatchApp(api_key, api_base)
        app.load_listings("listings.json")
        tester = create_simple_tester(app)
    """
    
    # Validate the app has listings
    if not hasattr(app, 'listings') or not app.listings:
        print("⚠️ WARNING: No listings found in HomeMatchApp")
        print("💡 Make sure to generate or load listings first:")
        print("   app.generate_listings(10)")
        print("   # or")  
        print("   app.load_listings('listings.json')")
        print()
    
    # Create tester instance
    tester = SimpleHomeMatchTester(app)
    
    # Create and display examples
    examples_widget = QuickExamples.create_widget(tester)
    display(examples_widget)
    
    # Display main tester
    tester.display()
    
    # Show usage tips in a collapsible format
    tips = widgets.HTML("""
    <div style='background: #f0f7ff; padding: 20px; border-radius: 10px; margin-top: 20px; border-left: 4px solid #007acc;'>
        <h4>🎯 How to Use This Tester:</h4>
        <ol style='margin-left: 20px;'>
            <li><strong>Click an example</strong> above or type your own query in the text area</li>
            <li><strong>Adjust max results</strong> if needed (1-5 properties)</li>
            <li><strong>Click "🔍 Search"</strong> to find matching properties</li>
            <li><strong>Click "✨ Personalize"</strong> to see custom descriptions</li>
            <li><strong>Use "🧹 Clear"</strong> to reset the output area</li>
        </ol>       
    </div>
    """)
    display(tips)
    
    return tester


# Convenience function for quick setup
def quick_test_setup(api_key, api_base=None, generate_new=False):
    """
    Quick setup function that creates app, loads data, and shows tester
    
    Args:
        api_key: OpenAI API key
        api_base: Optional API base URL
        generate_new: If True, generates new listings; if False, tries to load existing
    
    Returns:
        tuple: (app, tester) instances
    """
    from services import HomeMatchApp
    
    print("🚀 Setting up HomeMatch quick test environment...")
    
    # Initialize app
    app = HomeMatchApp(api_key, api_base)
    
    # Load or generate data
    if generate_new:
        print("🛠 Generating new listings...")
        success = app.generate_listings(10)
        if success:
            app.save_listings("test_listings.json")
    else:
        try:
            print("📂 Loading existing listings...")
            app.load_listings("listings.json")
        except FileNotFoundError:
            print("📁 No existing listings found, generating new ones...")
            success = app.generate_listings(10)
            if success:
                app.save_listings("listings.json")
    
    # Create tester
    tester = create_simple_tester(app)
    
    print("✅ Setup complete! Ready for testing.")
    return app, tester


