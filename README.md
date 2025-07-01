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
