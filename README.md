# 🔥 Microwave Cooking Time Converter

A responsive, mobile-friendly static web app that helps users convert microwave cooking times between different wattages. Built as a Progressive Web App (PWA) with offline functionality.

## 🚀 Live Demo

Visit the app: **[https://jtracey93.github.io/microwave-converter](https://jtracey93.github.io/microwave-converter)**

## ✨ Features

- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **PWA Support**: Install as an app on your device for offline use
- **Quick Selects**: Common wattages and cooking times for faster input
- **Real-time Validation**: Immediate feedback on input values
- **Clean UI**: Modern, minimalist design with intuitive navigation
- **Keyboard Shortcuts**: Enter to calculate, Escape to reset

## 🧮 How It Works

The app uses the standard microwave conversion formula:
```
New Time = (Original Time × Recipe Wattage) ÷ Your Wattage
```

Simply enter:
1. The wattage specified in your recipe
2. The cooking time from the recipe
3. Your microwave's actual wattage

Get the adjusted cooking time instantly!

## 🛠️ Technology Stack

- **HTML5** - Semantic markup
- **CSS3** - Modern styling with Grid and Flexbox
- **Vanilla JavaScript** - No frameworks, pure ES6+
- **PWA** - Service Worker for offline functionality
- **GitHub Pages** - Static hosting
- **Python MCP Server** - Model Context Protocol server for IDE integration

## 🚀 Deployment

This app is automatically deployed to GitHub Pages using GitHub Actions. Every push to the `main` branch triggers a new deployment.

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/jtracey93/microwave-converter.git
   cd microwave-converter
   ```

2. Start a local server:
   ```bash
   # Using Python 3
   python -m http.server 8000
   
   # Or using npm
   npm start
   ```

3. Open http://localhost:8000 in your browser

## 🤖 MCP Server Usage

This repository includes a Python MCP (Model Context Protocol) server that provides the same microwave time conversion capabilities via an MCP tool. This allows you to use the conversion functionality directly from IDEs like VS Code with MCP support.

### Setup MCP Server

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the MCP server:
   ```bash
   python mcp_server.py
   ```

### MCP Tool Usage

The MCP server provides the `convert_microwave_time` tool for microwave time conversion:

**Tool Parameters:**
- `original_wattage` (number): Recipe's microwave wattage (100-2000W)
- `target_wattage` (number): Your microwave's wattage (100-2000W)  
- `original_minutes` (number): Original cooking time in minutes (0-60)
- `original_seconds` (number): Original cooking time in seconds (0-59)

**Example tool call:**
```json
{
  "original_wattage": 1000,
  "target_wattage": 700,
  "original_minutes": 2,
  "original_seconds": 0
}
```

**Example response:**
```json
{
  "converted_time": {
    "minutes": 2,
    "seconds": 51,
    "total_seconds": 171,
    "formatted": "2m 51s"
  },
  "original_time": {
    "minutes": 2,
    "seconds": 0,
    "total_seconds": 120,
    "formatted": "2m 0s"
  },
  "wattages": {
    "original": 1000,
    "target": 700,
    "ratio": 1.43
  },
  "power_recommendation": {
    "power_level": "100%",
    "reason": "Your microwave power is similar to the recipe. Use normal power."
  },
  "explanation": "Cook for 2m 51s instead of 2m 0s when using a 700W microwave instead of 1000W"
}
```

### Testing the MCP Server

You can test the conversion logic without MCP dependencies:

```bash
python test_standalone.py
```

### VS Code Integration

To use this MCP server with VS Code, you'll need an MCP-compatible extension. Here are the steps:

1. **Install an MCP Extension**: Install an extension that supports the Model Context Protocol, such as:
   - [MCP Manager](https://marketplace.visualstudio.com/items?itemName=modelcontextprotocol.mcp-manager) (if available)
   - Or other MCP-compatible extensions from the VS Code marketplace

2. **Configure the MCP Server**: Add the microwave converter server to your MCP configuration. This is typically done through the extension's settings or a configuration file:

   ```json
   {
     "servers": {
       "microwave-converter": {
         "command": "python",
         "args": ["mcp_server.py"],
         "cwd": "/path/to/microwave-converter"
       }
     }
   }
   ```

3. **Update the Path**: Replace `/path/to/microwave-converter` with the actual path to this repository on your system.

4. **Start Using**: Once configured, you can use the microwave time conversion tool directly from VS Code through the MCP extension interface.

The MCP server will be available as a tool that you can call with cooking time conversion requests, making it easy to get microwave timing adjustments without leaving your development environment.

### Manual Deployment to GitHub Pages

1. Enable GitHub Pages in your repository settings
2. Set source to "GitHub Actions"
3. Push to main branch - deployment happens automatically

## 📱 PWA Installation

Users can install this app on their devices:

- **Desktop**: Click the install button in the address bar
- **Mobile**: Use "Add to Home Screen" option in browser menu
- **Works Offline**: Once installed, works without internet connection

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test locally
5. Commit: `git commit -m 'Add some feature'`
6. Push: `git push origin feature-name`
7. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🍳 Perfect for:

- Home cooks adjusting recipes
- College students with basic microwaves
- Anyone with a different wattage microwave than recipe calls for
- Quick conversions without complicated calculations

---

**Built with ❤️ for better cooking experiences**
