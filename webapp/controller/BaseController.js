sap.ui.define([
    "sap/ui/core/mvc/Controller",
    "sap/ui/core/routing/History"
], function (Controller, History) {
    "use strict";

    return Controller.extend("tech.trends.radar.controller.BaseController", {
        /**
         * Get the router for this component
         * @returns {sap.m.routing.Router} The router instance
         */
        getRouter: function () {
            return this.getOwnerComponent().getRouter();
        },

        /**
         * Get a model by name
         * @param {string} sName - The model name
         * @returns {sap.ui.model.Model} The model instance
         */
        getModel: function (sName) {
            return this.getView().getModel(sName);
        },

        /**
         * Set a model on the view
         * @param {sap.ui.model.Model} oModel - The model instance
         * @param {string} sName - The model name
         */
        setModel: function (oModel, sName) {
            return this.getView().setModel(oModel, sName);
        },

        /**
         * Get the resource bundle for i18n
         * @returns {sap.base.i18n.ResourceBundle} The resource bundle
         */
        getResourceBundle: function () {
            return this.getOwnerComponent().getModel("i18n").getResourceBundle();
        },

        /**
         * Get a text from the i18n resource bundle
         * @param {string} sKey - The i18n key
         * @param {Array} aArgs - Optional arguments for text formatting
         * @returns {string} The translated text
         */
        getText: function (sKey, aArgs) {
            return this.getResourceBundle().getText(sKey, aArgs);
        },

        /**
         * Navigate to a route
         * @param {string} sRouteName - The route name
         * @param {object} oParameters - Optional route parameters
         * @param {boolean} bReplace - Replace the hash instead of adding
         */
        navTo: function (sRouteName, oParameters, bReplace) {
            this.getRouter().navTo(sRouteName, oParameters, bReplace);
        },

        /**
         * Navigate back or to a fallback route
         * @param {string} sFallbackRoute - Fallback route if no history
         */
        onNavBack: function (sFallbackRoute) {
            var oHistory = History.getInstance();
            var sPreviousHash = oHistory.getPreviousHash();

            if (sPreviousHash !== undefined) {
                window.history.go(-1);
            } else if (sFallbackRoute) {
                this.navTo(sFallbackRoute, {}, true);
            } else {
                this.navTo("radar", {}, true);
            }
        }
    });
});
