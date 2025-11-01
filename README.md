# 🏗️ Architecture Diagram Generator

A powerful web application that converts natural language architecture descriptions into beautiful visual diagrams using **Google Gemini AI** and the **diagrams-as-code** library.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.0+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🤖 **AI-Powered**: Uses Google Gemini AI to generate diagram code from natural language
- 🎨 **Beautiful Diagrams**: Creates professional architecture diagrams automatically
- ☁️ **Multi-Cloud Support**: AWS, Kubernetes, and generic infrastructure components
- 🚀 **Easy to Use**: Simple web interface, no coding required
- 📊 **Code Export**: View and download the generated Python code
- 🌐 **Deploy Anywhere**: Run locally or deploy to Streamlit Cloud

## 🎯 Supported Components

### Cloud Providers
- **AWS**: EC2, Lambda, ECS, EKS, RDS, DynamoDB, S3, CloudFront, API Gateway, ALB, SQS, SNS, and more
- **Kubernetes**: Pods, Deployments, Services, Ingress, StatefulSets

### Databases & Caching
- PostgreSQL, MySQL, MongoDB, Cassandra, Redis, Memcached

### Message Queues
- Kafka, RabbitMQ, SQS, SNS, Celery

### Monitoring
- Prometheus, Grafana, Datadog, Splunk

### Programming Frameworks
- React, Django, FastAPI, Spring, Flask

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Graphviz** (required for diagram rendering)
   - **Windows**: Download from [Graphviz Downloads](https://graphviz.org/download/) and add to PATH
   - **macOS**: `brew install graphviz`
   - **Linux**: `sudo apt-get install graphviz`
3. **Google Gemini API Key** - Get one free from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Local Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Prompt-Architecture-Diagram
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key** (Optional but recommended)
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your API key
   # On Windows PowerShell:
   # notepad .env
   ```

4. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Open your browser** to `http://localhost:8501`

## ☁️ Deploy to Streamlit Cloud

### Step 1: Prepare Your Repository

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository and branch
5. Set **Main file path** to: `streamlit_app.py`
6. Click "Deploy"

### Step 3: Add Your API Key (Secrets)

1. In Streamlit Cloud, go to your app settings
2. Click on "Secrets" in the left sidebar
3. Add your API key in TOML format:
   ```toml
   GEMINI_API_KEY = "your_actual_api_key_here"
   ```
4. Click "Save"

Your app will automatically redeploy and be ready to use! 🎉

### Alternative: Use Sidebar Input

If you prefer not to use secrets, users can simply enter their API key in the sidebar when using the app.

## 📖 Usage Examples

### Example 1: Microservices Architecture
```
Create a microservices architecture with:
- Users connecting through a load balancer
- API Gateway routing to three microservices: User Service, Order Service, and Payment Service
- Each microservice has its own database
- A message queue (Kafka) for async communication between services
- Redis cache for the User Service
```

### Example 2: AWS Serverless
```
Create a serverless application using API Gateway, Lambda functions, DynamoDB,
S3 for file storage, and CloudFront for CDN
```

### Example 3: Three-Tier Web Application
```
Create a three-tier web application on AWS with ALB, EC2 instances in multiple
availability zones, RDS database with read replica, and S3 for static content
```

### Example 4: Event-Driven System
```
Create an event-driven system with EventBridge for routing, Lambda for processing,
SQS for queuing, SNS for notifications, and DynamoDB for state
```

### Example 5: Kubernetes Microservices
```
Design a Kubernetes-based microservices architecture with ingress controller,
3 microservices in separate pods, Redis cache, PostgreSQL database, and monitoring
with Prometheus
```

## 💡 Tips for Better Diagrams

1. **Be Specific**: Mention exact service names (e.g., "DynamoDB" not just "database")
2. **Include Relationships**: Describe how components connect and communicate
3. **Specify Infrastructure**: Mention if it's AWS, Kubernetes, or generic
4. **Add Details**: Include load balancers, caches, message queues, etc.
5. **Describe Flow**: Explain data flow and request/response patterns

## 🛠️ Project Structure

```
Prompt-Architecture-Diagram/
├── streamlit_app.py          # Main Streamlit application
├── app.py                    # Original Colab version
├── requirements.txt          # Python dependencies
├── packages.txt              # System dependencies (Graphviz)
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── .env.example             # Example environment variables
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```env
GEMINI_API_KEY=your_api_key_here
```

### Streamlit Configuration

The `.streamlit/config.toml` file contains UI theming and server settings. Modify as needed:

```toml
[theme]
primaryColor = "#2563EB"
backgroundColor = "#FFFFFF"
```

## 📦 Dependencies

- **streamlit**: Web application framework
- **google-generativeai**: Google Gemini AI SDK
- **diagrams**: Diagrams-as-code library
- **pillow**: Image processing
- **python-dotenv**: Environment variable management
- **graphviz**: Graph visualization (system package)

## 🐛 Troubleshooting

### "Graphviz not found" Error
- **Solution**: Install Graphviz and add it to your system PATH
- **Windows**: After installation, add `C:\Program Files\Graphviz\bin` to PATH
- **Verify**: Run `dot -V` in terminal to check installation

### "Invalid API key" Error
- **Solution**: Verify your Gemini API key is correct
- Get a new key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Diagram Generation Fails
- **Solution**: Try simplifying your description
- Check the generated code for any import errors
- Some component names are case-sensitive (e.g., use "Dynamodb" not "DynamoDB")

### Deployment Issues on Streamlit Cloud
- Ensure `packages.txt` contains `graphviz`
- Verify your secrets are properly set in Streamlit Cloud
- Check app logs for specific error messages

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for powerful code generation
- **diagrams library** by mingrammer for the amazing diagrams-as-code tool
- **Streamlit** for the excellent web framework

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for developers and architects**

⭐ If you find this useful, please star the repository!
