## Project Setup
When creating a new SAPUI5 application:
- Use Easy-UI5 generator (yo easy-ui5 project) for quick setup
- Or manually create structure: webapp/, Component.js, manifest.json, index.html
- Install UI5 CLI as dev dependency
- Verify with npm start that "Hello World" displays

**Required tools:**
- Node.js v20.11.0+ or v22.0.0+
- UI5 CLI (@ui5/cli)
- UI5 Linter (@ui5/linter)

## Component Structure
When building the application:
- Component.js initializes the app and router
- manifest.json declares configuration, models, and routing
- App.view.xml contains Shell and App container
- BaseController provides common utilities (getRouter, getModel, getText, navTo, onNavBack)
- Use i18n for all user-facing text

## Data Models
When connecting to data:
- Start with JSON model and mock data for development
- Use formatters for data transformation (webapp/model/formatter.js)
- Switch to OData V4 model when backend is ready
- Configure dataSource in manifest.json sap.app section
- Add proxy middleware in ui5.yaml for local development

**OData V4 model settings:**
- synchronizationMode: "None"
- operationMode: "Server"
- autoExpandSelect: true
- earlyRequests: true

## Navigation and Routing
When adding multiple views:
- Configure routing in manifest.json sap.ui5.routing section
- Define routes with name, pattern, and target
- Define targets with view names
- Initialize router in Component.js init method
- Use navTo() for navigation, attachPatternMatched for route handling
- Implement onNavBack in BaseController

## Testing
When adding tests:
- Create test/unit/ for QUnit unit tests
- Create test/integration/ for OPA5 integration tests
- Test formatters and model logic with unit tests
- Test user journeys with OPA5 page objects and journeys
- Run tests via testsuite.qunit.html

## Code Quality
When preparing for production:
- Run ui5lint and fix all errors
- Ensure async loading everywhere (data-sap-ui-async="true")
- Remove deprecated API usage (no jQuery.sap, no sync loading)
- Use sap.ui.define for all modules
- Check manifest version for UI5 2.x compatibility

## Building and Deployment
When deploying the application:
- Build with: npx ui5 build --clean-dest --all
- Output goes to dist/ folder with Component-preload.js
- For ABAP: use deploy-to-abap custom task
- For BTP: create mta.yaml and deploy with cf deploy
- For static hosting: deploy dist/ folder contents

## Troubleshooting
When the app won't start:
- Run ui5lint to check for syntax errors
- Check browser console for errors
- Verify manifest.json is valid JSON
- Check Component.js namespace matches manifest

**When data doesn't load:**
- Check Network tab for failed requests
- Verify dataSource URI in manifest.json
- Check proxy configuration in ui5.yaml

**When routing fails:**
- Verify controlId matches App control ID in manifest
- Check route patterns don't conflict
- Ensure router.initialize() is called in Component.js