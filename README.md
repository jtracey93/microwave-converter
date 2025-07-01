# 🔥 Microwave Time Converter

A responsive static web app that helps users convert microwave cooking times between different wattages. Built with vanilla HTML, CSS, and JavaScript, optimized for mobile devices and ready for Azure Static Web Apps deployment.

## Features

- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Real-time Validation**: Input validation with helpful error messages
- **PWA Ready**: Installable as a Progressive Web App with offline capabilities
- **Intuitive Interface**: Clean, modern UI with smooth animations
- **Quick Select**: Common wattage buttons for faster input
- **Detailed Results**: Clear explanations of the conversion calculations

## How It Works

The app uses the energy equivalency formula to convert cooking times:

```
New Time = (Original Time × Recipe Wattage) ÷ Your Wattage
```

This ensures that the same amount of energy is delivered to your food, regardless of the microwave's wattage.

## Usage

1. Enter the wattage specified in the cooking instructions
2. Input the cooking time (minutes and seconds)
3. Enter your microwave's wattage
4. Click "Calculate Cooking Time" to get the adjusted time

## Technologies Used

- **HTML5**: Semantic markup with accessibility features
- **CSS3**: Modern styling with CSS Grid, Flexbox, and animations
- **JavaScript (ES6+)**: Vanilla JavaScript with modern features
- **Progressive Web App**: Service worker for offline functionality
- **Font Awesome**: Icons for enhanced UI
- **Google Fonts**: Poppins font family

## Deployment

This app is designed to be deployed on Azure Static Web Apps:

### Prerequisites

```bash
npm install -g @azure/static-web-apps-cli
```

### Local Development

```bash
# Start local development server
npx swa start

# Build for production
npx swa build
```

### Deploy to Azure

```bash
# Deploy to production environment
npx swa deploy --env production
```

## Project Structure

```
microwave-converter/
├── index.html          # Main HTML file
├── styles.css          # Responsive CSS styles
├── script.js           # JavaScript functionality
├── sw.js              # Service Worker for PWA
├── manifest.json      # Web App Manifest
├── swa-cli.config.json # Static Web Apps configuration
└── README.md          # Project documentation
```

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on multiple devices
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Mathematical formula based on standard microwave energy conversion principles
- Icons provided by Font Awesome
- Fonts provided by Google Fonts
- Built following Azure Static Web Apps best practices
A static web app that converts cooking times between different microwave wattages
