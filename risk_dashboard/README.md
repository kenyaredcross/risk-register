# KRCS Risk Management Dashboard

A stunning Vue 3 dashboard for the Kenya Red Cross Society Risk Management System.

## Design Features

- **Color Scheme**: White (90%), Black (8%), Red (2%)
- **Modern Minimalist**: Clean, card-based layout with elegant shadows
- **Smooth Animations**: Fade-in, slide-up, and scale transitions
- **Responsive**: Mobile-friendly design
- **Interactive Risk Matrix**: 5×5 heatmap with real-time calculations

## Technology Stack

- **Vue 3** - Composition API
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first styling
- **Pinia** - State management
- **Vue Router** - Client-side routing
- **Axios** - API integration with Frappe

## Development Setup

### Install Dependencies

```bash
cd /home/lnx/frappes/krcs-bench/apps/krcs_risk/krcs_risk/public/vue_dashboard
npm install
```

### Run Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:8081`

### Build for Production

```bash
npm run build
```

This creates optimized files in the `dist/` directory.

## Project Structure

```
vue_dashboard/
├── src/
│   ├── components/        # Reusable UI components
│   │   ├── StatsCard.vue
│   │   ├── RiskMatrix.vue
│   │   └── RiskCard.vue
│   ├── views/            # Page components
│   │   ├── Dashboard.vue
│   │   ├── RiskList.vue
│   │   └── RiskDetail.vue
│   ├── composables/      # Reusable logic
│   │   └── useApi.js
│   ├── stores/           # Pinia stores
│   │   └── riskStore.js
│   ├── router/           # Vue Router config
│   │   └── index.js
│   ├── assets/           # CSS and static files
│   │   └── main.css
│   └── App.vue           # Root component
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## Features

### Dashboard View
- Statistics cards showing total, critical, high, medium, and low risks
- Interactive 5×5 risk matrix heatmap
- Recent risks display
- Color-coded risk levels

### Risk Register View
- Complete list of all risks
- Search functionality
- Filters by risk level and status
- Sorting options
- Responsive grid layout

### Risk Detail View
- Full risk information
- Assessment metrics (likelihood, impact, rating)
- Possible causes and consequences
- Mitigating actions
- Quick info sidebar
- Edit link to Frappe

## Integration with Frappe

The dashboard integrates with Frappe's REST API:

- **Endpoint**: `/api/resource/Program Risk Register`
- **Authentication**: Uses Frappe session cookies
- **CSRF Protection**: Automatically handled

## Color Palette

```javascript
// Primary
White: #FFFFFF
Off-White: #FAFAFA
Light Gray: #F5F5F5

// Black Variants
Black: #000000
Charcoal: #1A1A1A
Dark Gray: #2D2D2D

// Red Accents (Strategic Use)
Red Primary: #DC2626    // Critical risks, CTAs
Red Hover: #B91C1C
Red Light: #FEE2E2

// Risk Levels
Low: #10B981 (Green)
Medium: #F59E0B (Yellow)
High: #F97316 (Orange)
Critical: #DC2626 (Red)
```

## Animations

- **fade-in**: 0.5s ease-in-out
- **slide-up**: 0.4s ease-out
- **scale-in**: 0.3s ease-out
- **pulse-red**: For critical risk indicators

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers

## License

Copyright (c) 2026, KRCS
