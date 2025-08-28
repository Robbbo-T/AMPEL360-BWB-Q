# AMPEL360 Interactive Framework Deployment

This directory contains the interactive web-based navigation interface for the AMPEL360 H₂-BWB-Q Optimization Framework.

## Quick Start

### Local Development
1. Open `index.html` in a modern web browser
2. Or serve via a local web server:
   ```bash
   # Python 3
   python -m http.server 8000
   
   # Python 2
   python -m SimpleHTTPServer 8000
   
   # Node.js (if you have http-server installed)
   npx http-server
   ```
3. Navigate to `http://localhost:8000`

### Static Deployment
The interactive index is built as a static web application and can be deployed to any static hosting service:

- **GitHub Pages**: Commit the files and enable GitHub Pages on the repository
- **Netlify**: Drag and drop the OPTIM-FRAMEWORK folder to Netlify
- **Vercel**: Connect the repository and set build output to `OPTIM-FRAMEWORK/`
- **AWS S3**: Upload files to an S3 bucket configured for static website hosting

## Features

### 🏠 Interactive Navigation
- **Overview**: Card-based navigation to main framework sections
- **Structure**: Expandable tree view of the complete directory structure  
- **Technological Domains**: Grid view of all technical domains with descriptions
- **Quick Access**: Direct links to documentation, tools, and configurations

### 🔍 Smart Search
- Real-time search across all framework components
- Keyboard shortcut: `Ctrl+K` (or `Cmd+K` on Mac)
- Search domains, documentation, tools, and configurations
- Press `Escape` to clear search

### 📱 Responsive Design
- Mobile-friendly interface
- Adaptive grid layouts
- Touch-friendly navigation
- Progressive enhancement

## File Structure

```
OPTIM-FRAMEWORK/
├── index.html          # Main interactive interface
├── styles.css          # CSS styling and responsive design
├── script.js           # JavaScript functionality
├── DEPLOYMENT.md       # This file
└── README.md           # Framework documentation
```

## Technology Stack

- **HTML5**: Semantic structure and accessibility
- **CSS3**: Modern styling with CSS Grid and Flexbox
- **Vanilla JavaScript**: No dependencies, fast loading
- **Font Awesome**: Icons for better visual hierarchy
- **Progressive Enhancement**: Works without JavaScript

## Browser Support

- ✅ Chrome 60+
- ✅ Firefox 55+
- ✅ Safari 12+
- ✅ Edge 79+
- ⚠️ Internet Explorer: Not supported (uses modern CSS Grid)

## Customization

### Adding New Domains
Edit `script.js` and update the `getTechnologicalDomains()` function:

```javascript
{
    id: 'NEW-DOMAIN',
    name: 'NEW-DOMAIN-NAME',
    description: 'Domain description here.',
    icon: 'fas fa-icon-name'
}
```

### Styling Changes
Modify CSS custom properties in `styles.css`:

```css
:root {
    --primary-color: #2c3e50;
    --secondary-color: #3498db;
    /* Add your colors here */
}
```

### Adding Search Items
Update the `getSearchResults()` function in `script.js` to include new searchable content.

## Performance

The interactive index is optimized for performance:
- **< 100KB total size**: Fast loading even on slow connections
- **No external dependencies**: Everything loads from local files
- **Lazy loading**: Search results load on demand
- **Optimized images**: SVG icons for crisp display at any size

## Accessibility

- **Keyboard Navigation**: Full keyboard support
- **Screen Reader Friendly**: Semantic HTML and ARIA labels
- **High Contrast**: Meets WCAG 2.1 AA standards
- **Focus Management**: Clear focus indicators

## Deployment Examples

### GitHub Pages
1. Ensure `index.html` is in the repository root or docs folder
2. Go to repository Settings > Pages
3. Select source branch and folder
4. Site will be available at `https://username.github.io/repository-name/`

### Netlify
1. Drag the OPTIM-FRAMEWORK folder to [Netlify's deploy page](https://app.netlify.com/drop)
2. Or connect your Git repository for automatic deployments
3. Site will be assigned a random subdomain or use a custom domain

### AWS S3 + CloudFront
```bash
# Sync files to S3
aws s3 sync . s3://your-bucket-name --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"
```

## Monitoring and Analytics

To add analytics tracking, include your tracking code in `index.html`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_TRACKING_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_TRACKING_ID');
</script>
```

## Maintenance

The interactive index automatically reflects the current directory structure. When adding new domains or components:

1. **Create the directory structure** following UTCS conventions
2. **Add README.md files** in each component for documentation
3. **Update the domain mapping** in `script.js` if needed
4. **Test all links** to ensure navigation works correctly

## Security

For production deployments:
- **HTTPS Only**: Always deploy with SSL/TLS encryption
- **Content Security Policy**: Consider adding CSP headers
- **Regular Updates**: Keep the interface updated with framework changes

## Support

For issues with the interactive index:
1. Check browser console for JavaScript errors
2. Verify all file paths are correct and accessible
3. Test with different browsers to isolate compatibility issues
4. Review the deployment logs for any server-side issues

---

*Generated by the AMPEL360 H₂-BWB-Q Interactive Framework Index System*