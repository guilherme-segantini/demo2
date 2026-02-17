sap.ui.define([
    "./BaseController",
    "sap/ui/model/json/JSONModel",
    "sap/ui/model/Filter",
    "sap/ui/model/FilterOperator"
], function (BaseController, JSONModel, Filter, FilterOperator) {
    "use strict";

    return BaseController.extend("tech.trends.radar.controller.RadarView", {
        onInit: function () {
            // Wait for radar model to load data
            var oComponent = this.getOwnerComponent();
            if (oComponent) {
                var oRadarModel = oComponent.getModel("radar");
                if (oRadarModel) {
                    oRadarModel.attachRequestCompleted(this._onDataLoaded, this);
                    // If data already loaded, process it
                    if (oRadarModel.getData() && oRadarModel.getData().trends) {
                        this._onDataLoaded();
                    }
                }
            }
        },

        _onDataLoaded: function () {
            var oRadarModel = this.getOwnerComponent().getModel("radar");
            var oData = oRadarModel.getData();

            if (!oData || !oData.trends) {
                return;
            }

            // Create filtered models for each focus area
            this._createFocusAreaModels(oData.trends);
        },

        _createFocusAreaModels: function (aTrends) {
            var oView = this.getView();

            // Filter trends by focus area and classification
            var oVoiceAiSignals = aTrends.filter(function (oTrend) {
                return oTrend.focus_area === "voice_ai_ux" && oTrend.classification === "signal";
            });
            var oVoiceAiNoise = aTrends.filter(function (oTrend) {
                return oTrend.focus_area === "voice_ai_ux" && oTrend.classification === "noise";
            });

            var oAgentOrchSignals = aTrends.filter(function (oTrend) {
                return oTrend.focus_area === "agent_orchestration" && oTrend.classification === "signal";
            });
            var oAgentOrchNoise = aTrends.filter(function (oTrend) {
                return oTrend.focus_area === "agent_orchestration" && oTrend.classification === "noise";
            });

            var oDurableRuntimeSignals = aTrends.filter(function (oTrend) {
                return oTrend.focus_area === "durable_runtime" && oTrend.classification === "signal";
            });
            var oDurableRuntimeNoise = aTrends.filter(function (oTrend) {
                return oTrend.focus_area === "durable_runtime" && oTrend.classification === "noise";
            });

            // Set models on view
            oView.setModel(new JSONModel({ items: oVoiceAiSignals }), "voiceAiSignals");
            oView.setModel(new JSONModel({ items: oVoiceAiNoise }), "voiceAiNoise");
            oView.setModel(new JSONModel({ items: oAgentOrchSignals }), "agentOrchSignals");
            oView.setModel(new JSONModel({ items: oAgentOrchNoise }), "agentOrchNoise");
            oView.setModel(new JSONModel({ items: oDurableRuntimeSignals }), "durableRuntimeSignals");
            oView.setModel(new JSONModel({ items: oDurableRuntimeNoise }), "durableRuntimeNoise");
        }
    });
});
