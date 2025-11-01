"""
Architecture Diagram Generator using Gemini AI and diagrams-as-code
Streamlit Web Application
"""

import streamlit as st
import os
import re
import ast
import tempfile
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from diagrams import Diagram, Cluster, Edge

# Load environment variables
load_dotenv()

# Comprehensive mapping of available components
AVAILABLE_COMPONENTS = {
    # AWS Compute
    'diagrams.aws.compute': ['EC2', 'Lambda', 'ECS', 'EKS', 'Batch', 'Fargate', 'ElasticBeanstalk'],
    
    # AWS Database
    'diagrams.aws.database': ['RDS', 'Dynamodb', 'Aurora', 'Elasticache', 'ElastiCache', 
                              'DocumentdbMongodbCompatibility', 'Neptune', 'Redshift', 'Timestream'],
    
    # AWS Network
    'diagrams.aws.network': ['ELB', 'ALB', 'NLB', 'CloudFront', 'Route53', 'APIGateway', 
                            'VPC', 'DirectConnect', 'CloudMap'],
    
    # AWS Storage
    'diagrams.aws.storage': ['S3', 'EBS', 'EFS', 'Backup', 'StorageGateway', 'Fsx'],
    
    # AWS Integration - IMPORTANT: No EventBridge!
    'diagrams.aws.integration': ['SQS', 'SNS', 'StepFunctions', 'Eventbridge', 'MQ', 
                                'Appsync', 'ExpressWorkflows'],
    
    # Generic/OnPrem
    'diagrams.onprem.client': ['User', 'Client'],
    'diagrams.onprem.database': ['PostgreSQL', 'MySQL', 'MongoDB', 'Cassandra', 'Mariadb'],
    'diagrams.onprem.inmemory': ['Redis', 'Memcached'],
    'diagrams.onprem.queue': ['Kafka', 'RabbitMQ', 'Celery', 'Activemq'],
    'diagrams.onprem.monitoring': ['Prometheus', 'Grafana', 'Datadog', 'Splunk'],
    
    # Programming
    'diagrams.programming.framework': ['React', 'Django', 'FastAPI', 'Spring', 'Flask'],
    'diagrams.programming.language': ['Python', 'Java', 'NodeJS', 'Go', 'Javascript'],
    
    # Kubernetes
    'diagrams.k8s.compute': ['Pod', 'Deployment', 'StatefulSet', 'Job', 'DaemonSet'],
    'diagrams.k8s.network': ['Ingress', 'Service'],
    'diagrams.k8s.storage': ['PV', 'PVC', 'StorageClass'],
}

# Common naming mistakes and their corrections
NAMING_FIXES = {
    'DynamoDB': 'Dynamodb',
    'ElastiCache': 'Elasticache',
    'EventBridge': 'Eventbridge',
    'StepFunction': 'StepFunctions',
    'Users': 'User',
    'Clients': 'Client',
    'NodeJS': 'NodeJS',  # Already correct
    'from diagrams.onprem.client import Users': 'from diagrams.onprem.client import User',
    'from diagrams.onprem.client import Clients': 'from diagrams.onprem.client import Client',
    'from diagrams.aws.database import DynamoDB': 'from diagrams.aws.database import Dynamodb',
    'from diagrams.aws.database import ElastiCache': 'from diagrams.aws.database import Elasticache',
    'from diagrams.aws.integration import EventBridge': 'from diagrams.aws.integration import Eventbridge',
}

def setup_gemini(api_key):
    """Setup Gemini API with the provided key"""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash-exp')

def get_component_list_for_prompt():
    """Generate a formatted list of available components for the prompt"""
    component_list = []
    
    for module, components in AVAILABLE_COMPONENTS.items():
        component_list.append(f"\n{module}:")
        component_list.append(f"  Available: {', '.join(components)}")
    
    return '\n'.join(component_list)

def validate_and_fix_imports(code):
    """Validate imports and fix common issues"""
    
    # First, apply common naming fixes
    for old, new in NAMING_FIXES.items():
        code = code.replace(old, new)
    
    # Parse the code to extract imports
    try:
        tree = ast.parse(code)
        imports_to_fix = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module
                if module and module.startswith('diagrams.'):
                    for alias in node.names:
                        component_name = alias.name
                        
                        # Check if this component exists in our mapping
                        if module in AVAILABLE_COMPONENTS:
                            if component_name not in AVAILABLE_COMPONENTS[module]:
                                # Find similar component or remove it
                                similar = find_similar_component(component_name, AVAILABLE_COMPONENTS[module])
                                if similar:
                                    imports_to_fix.append((component_name, similar))
        
        # Apply fixes
        for old_name, new_name in imports_to_fix:
            code = code.replace(f'import {old_name}', f'import {new_name}')
            code = code.replace(f'{old_name}(', f'{new_name}(')
            
    except SyntaxError:
        pass
    
    return code

def find_similar_component(name, available_components):
    """Find a similar component name in the available list"""
    name_lower = name.lower()
    
    for component in available_components:
        if name_lower == component.lower():
            return component
        if name_lower in component.lower() or component.lower() in name_lower:
            return component
    
    return None

def generate_diagram_code(model, user_prompt, max_retries=2):
    """Generate Python code for diagram based on user description"""
    
    system_prompt = f"""You are an expert in creating architecture diagrams using Python's 'diagrams' library.

AVAILABLE COMPONENTS - USE ONLY THESE EXACT NAMES:
{get_component_list_for_prompt()}

CRITICAL RULES:
1. Use ONLY components listed above with EXACT names
2. NEVER use 'EventBridge' - use 'Eventbridge' instead
3. NEVER use 'DynamoDB' - use 'Dynamodb' instead
4. NEVER use 'ElastiCache' - use 'Elasticache' instead
5. NEVER use 'Users' - use 'User' instead
6. Always use show=False in Diagram()
7. Use proper connections: >> (left to right), << (right to left), or - (bidirectional)
8. Use Cluster for grouping related components
9. Set direction parameter: "LR" (left-right), "TB" (top-bottom), "BT", or "RL"

EXAMPLE (FOLLOW THIS EXACT PATTERN):
```python
from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda, ECS
from diagrams.aws.database import RDS, Dynamodb, Elasticache
from diagrams.aws.network import CloudFront, APIGateway
from diagrams.aws.integration import SQS, SNS, StepFunctions
from diagrams.onprem.client import User

with Diagram("E-commerce Platform", show=False, direction="LR"):
    customer = User("Customer")
    
    with Cluster("AWS Cloud"):
        cdn = CloudFront("CDN")
        api = APIGateway("API Gateway")
        
        with Cluster("Services"):
            auth = Lambda("Auth")
            products = ECS("Products")
        
        with Cluster("Data"):
            db = Dynamodb("User DB")
            cache = Elasticache("Cache")
        
        queue = SQS("Queue")
        topic = SNS("Notifications")
    
    customer >> cdn >> api >> auth
    api >> products >> [db, cache]
    products >> queue >> topic
```

IMPORTANT: If you need event-driven architecture, use 'Eventbridge' (lowercase 'bridge').
If you need step functions, use 'StepFunctions' (camelCase with 's').

Generate ONLY the Python code, no explanations."""

    full_prompt = f"{system_prompt}\n\nUser Description:\n{user_prompt}\n\nGenerate the diagram code:"
    
    for attempt in range(max_retries + 1):
        try:
            response = model.generate_content(full_prompt)
            code = response.text
            
            # Extract code from markdown if present
            if "```python" in code:
                code = re.search(r"```python\n(.*?)\n```", code, re.DOTALL).group(1)
            elif "```" in code:
                code = re.search(r"```\n(.*?)\n```", code, re.DOTALL).group(1)
            
            # Validate and fix imports
            code = validate_and_fix_imports(code)
            
            return code.strip()
        except Exception as e:
            if attempt < max_retries:
                continue
            else:
                raise e

def execute_diagram_code(code, output_dir):
    """Execute the generated diagram code and return the PNG file path"""
    try:
        # Change to output directory
        original_dir = os.getcwd()
        os.chdir(output_dir)
        
        # Create a namespace for execution
        namespace = {}
        
        # Execute the code
        exec(code, namespace)
        
        # Find the generated PNG file
        png_files = list(Path(output_dir).glob('*.png'))
        
        # Change back to original directory
        os.chdir(original_dir)
        
        if png_files:
            return True, str(png_files[0]), None
        else:
            return False, None, "PNG file not found after execution"
            
    except Exception as e:
        os.chdir(original_dir)
        return False, None, str(e)

# ============================================================================
# STREAMLIT UI
# ============================================================================

# Page Configuration
st.set_page_config(
    page_title="Architecture Diagram Generator",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextArea textarea {
        font-family: 'Courier New', monospace;
        font-size: 14px;
    }
    h1 {
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    h2 {
        color: #374151;
        font-weight: 600;
        margin-top: 1rem;
    }
    h3 {
        color: #4B5563;
        font-weight: 500;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #D1FAE5;
        border-left: 4px solid #10B981;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #DBEAFE;
        border-left: 4px solid #3B82F6;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #2563EB;
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 0.5rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("🏗️ Architecture Diagram Generator")
st.markdown("**Transform your architecture descriptions into beautiful diagrams using AI**")
st.markdown("---")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key Input
    default_key = os.getenv("GEMINI_API_KEY", "")
    api_key = st.text_input(
        "Google Gemini API Key", 
        value=default_key,
        type="password", 
        help="Enter your Google Gemini API key. Get one from Google AI Studio."
    )
    
    st.markdown("🔑 [Get API Key](https://makersuite.google.com/app/apikey)")
    
    st.markdown("---")
    
    # Example Prompts
    st.header("💡 Example Prompts")
    
    example_prompts = {
        "Microservices Architecture": """Create a microservices architecture with:
- Users connecting through a load balancer
- API Gateway routing to three microservices: User Service, Order Service, and Payment Service
- Each microservice has its own database
- A message queue (Kafka) for async communication between services
- Redis cache for the User Service""",
        
        "AWS Serverless": """Create a serverless application using API Gateway, Lambda functions, DynamoDB,
S3 for file storage, and CloudFront for CDN""",
        
        "Three-Tier Web App": """Create a three-tier web application on AWS with ALB, EC2 instances in multiple
availability zones, RDS database with read replica, and S3 for static content""",
        
        "Event-Driven System": """Create an event-driven system with EventBridge for routing, Lambda for processing,
SQS for queuing, SNS for notifications, and DynamoDB for state""",
        
        "Kubernetes Deployment": """Design a Kubernetes-based microservices architecture with ingress controller,
3 microservices in separate pods, Redis cache, PostgreSQL database, and monitoring
with Prometheus"""
    }
    
    selected_example = st.selectbox(
        "Choose an example:",
        ["None"] + list(example_prompts.keys())
    )
    
    if selected_example != "None":
        if st.button("Use This Example", use_container_width=True):
            st.session_state.user_prompt = example_prompts[selected_example]
            st.rerun()
    
    st.markdown("---")
    
    # About Section
    st.header("ℹ️ About")
    st.markdown("""
    This tool uses:
    - **Google Gemini AI** for code generation
    - **Diagrams library** for diagram rendering
    - **Graphviz** for graph visualization
    
    Supports AWS, Kubernetes, and generic infrastructure components.
    """)

# Main Content Area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 Input")
    
    # Initialize session state for prompt if not exists
    if 'user_prompt' not in st.session_state:
        st.session_state.user_prompt = ""
    
    user_prompt = st.text_area(
        "Describe your architecture:",
        value=st.session_state.user_prompt,
        height=350,
        placeholder="""Example:

Create a microservices architecture with:
- Users connecting through a load balancer
- API Gateway routing to three microservices
- Each microservice has its own database
- Redis cache for fast access
- Message queue for async communication

Be as detailed as you want!""",
        key="prompt_input"
    )
    
    # Update session state
    st.session_state.user_prompt = user_prompt
    
    generate_button = st.button("🚀 Generate Diagram", type="primary", use_container_width=True)
    
    # Show tips
    with st.expander("💡 Tips for better diagrams"):
        st.markdown("""
        - Be specific about the services and their relationships
        - Mention the type of infrastructure (AWS, Kubernetes, etc.)
        - Include data flow and communication patterns
        - Specify databases, caches, and message queues
        - Mention load balancers, CDNs, and API gateways
        """)

with col2:
    st.header("📊 Output")
    
    # Placeholder for outputs
    status_placeholder = st.empty()
    image_placeholder = st.empty()
    code_placeholder = st.empty()

# Generate diagram when button is clicked
if generate_button:
    if not api_key:
        status_placeholder.error("❌ Please enter your Gemini API key in the sidebar")
    elif not user_prompt:
        status_placeholder.error("❌ Please enter an architecture description")
    else:
        try:
            with status_placeholder:
                with st.spinner("🤖 Generating diagram code with Gemini AI..."):
                    # Setup Gemini
                    model = setup_gemini(api_key)
                    
                    # Generate code
                    diagram_code = generate_diagram_code(model, user_prompt)
                    
                    st.info("✅ Code generated! Now creating the diagram...")
                
            # Create temporary directory for output
            with tempfile.TemporaryDirectory() as temp_dir:
                # Execute code
                success, png_path, error = execute_diagram_code(diagram_code, temp_dir)
                
                if success:
                    status_placeholder.success("✅ Diagram generated successfully!")
                    
                    # Display image first (most important)
                    with image_placeholder:
                        st.image(png_path, use_container_width=True, caption="Generated Architecture Diagram")
                    
                    # Then show the code
                    with code_placeholder:
                        with st.expander("🔍 View Generated Python Code", expanded=False):
                            st.code(diagram_code, language="python")
                            
                            # Download button for code
                            st.download_button(
                                label="💾 Download Code",
                                data=diagram_code,
                                file_name="architecture_diagram.py",
                                mime="text/plain"
                            )
                else:
                    status_placeholder.error(f"❌ Error generating diagram: {error}")
                    
                    with code_placeholder:
                        with st.expander("🔍 View Generated Code (with errors)", expanded=True):
                            st.code(diagram_code, language="python")
                        
                        st.warning("💡 Try running again or simplify your description.")
                        
        except Exception as e:
            status_placeholder.error(f"❌ Error: {str(e)}")
            st.markdown("""
            **Common issues:**
            - Invalid API key
            - Network connection issues
            - Graphviz not installed (required for diagram rendering)
            """)

# Footer
st.markdown("---")
col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    st.markdown("**Built with:**")
    st.markdown("🤖 Google Gemini AI")
    
with col_f2:
    st.markdown("**Powered by:**")
    st.markdown("📊 Diagrams Library")
    
with col_f3:
    st.markdown("**Framework:**")
    st.markdown("⚡ Streamlit")

st.markdown("<p style='text-align: center; color: #6B7280; margin-top: 2rem;'>Made with ❤️ for developers and architects</p>", unsafe_allow_html=True)
