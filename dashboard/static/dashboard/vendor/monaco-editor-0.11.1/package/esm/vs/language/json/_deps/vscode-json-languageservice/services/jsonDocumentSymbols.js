/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/
'use strict';
import * as Strings from '../utils/strings.js';
import { colorFromHex } from '../utils/colors.js';
import { SymbolKind, Range, Location, TextEdit } from '../../vscode-languageserver-types/main.js';
var JSONDocumentSymbols = /** @class */ (function () {
    function JSONDocumentSymbols(schemaService) {
        this.schemaService = schemaService;
    }
    JSONDocumentSymbols.prototype.findDocumentSymbols = function (document, doc) {
        var _this = this;
        var root = doc.root;
        if (!root) {
            return null;
        }
        // special handling for key bindings
        var resourceString = document.uri;
        if ((resourceString === 'vscode://defaultsettings/keybindings.json') || Strings.endsWith(resourceString.toLowerCase(), '/user/keybindings.json')) {
            if (root.type === 'array') {
                var result_1 = [];
                root.items.forEach(function (item) {
                    if (item.type === 'object') {
                        var property = item.getFirstProperty('key');
                        if (property && property.value) {
                            var location = Location.create(document.uri, Range.create(document.positionAt(item.start), document.positionAt(item.end)));
                            result_1.push({ name: property.value.getValue(), kind: SymbolKind.Function, location: location });
                        }
                    }
                });
                return result_1;
            }
        }
        var collectOutlineEntries = function (result, node, containerName) {
            if (node.type === 'array') {
                node.items.forEach(function (node) {
                    collectOutlineEntries(result, node, containerName);
                });
            }
            else if (node.type === 'object') {
                var objectNode = node;
                objectNode.properties.forEach(function (property) {
                    var location = Location.create(document.uri, Range.create(document.positionAt(property.start), document.positionAt(property.end)));
                    var valueNode = property.value;
                    if (valueNode) {
                        var childContainerName = containerName ? containerName + '.' + property.key.value : property.key.value;
                        result.push({ name: property.key.getValue(), kind: _this.getSymbolKind(valueNode.type), location: location, containerName: containerName });
                        collectOutlineEntries(result, valueNode, childContainerName);
                    }
                });
            }
            return result;
        };
        var result = collectOutlineEntries([], root, void 0);
        return result;
    };
    JSONDocumentSymbols.prototype.getSymbolKind = function (nodeType) {
        switch (nodeType) {
            case 'object':
                return SymbolKind.Module;
            case 'string':
                return SymbolKind.String;
            case 'number':
                return SymbolKind.Number;
            case 'array':
                return SymbolKind.Array;
            case 'boolean':
                return SymbolKind.Boolean;
            default:// 'null'
                return SymbolKind.Variable;
        }
    };
    JSONDocumentSymbols.prototype.findDocumentColors = function (document, doc) {
        return this.schemaService.getSchemaForResource(document.uri, doc).then(function (schema) {
            var result = [];
            if (schema) {
                var matchingSchemas = doc.getMatchingSchemas(schema.schema);
                var visitedNode = {};
                for (var _i = 0, matchingSchemas_1 = matchingSchemas; _i < matchingSchemas_1.length; _i++) {
                    var s = matchingSchemas_1[_i];
                    if (!s.inverted && s.schema && (s.schema.format === 'color' || s.schema.format === 'color-hex') && s.node && s.node.type === 'string') {
                        var nodeId = String(s.node.start);
                        if (!visitedNode[nodeId]) {
                            var color = colorFromHex(s.node.getValue());
                            if (color) {
                                var range = Range.create(document.positionAt(s.node.start), document.positionAt(s.node.end));
                                result.push({ color: color, range: range });
                            }
                            visitedNode[nodeId] = true;
                        }
                    }
                }
            }
            return result;
        });
    };
    JSONDocumentSymbols.prototype.getColorPresentations = function (document, doc, color, range) {
        var result = [];
        var red256 = Math.round(color.red * 255), green256 = Math.round(color.green * 255), blue256 = Math.round(color.blue * 255);
        function toTwoDigitHex(n) {
            var r = n.toString(16);
            return r.length !== 2 ? '0' + r : r;
        }
        var label;
        if (color.alpha === 1) {
            label = "#" + toTwoDigitHex(red256) + toTwoDigitHex(green256) + toTwoDigitHex(blue256);
        }
        else {
            label = "#" + toTwoDigitHex(red256) + toTwoDigitHex(green256) + toTwoDigitHex(blue256) + toTwoDigitHex(Math.round(color.alpha * 255));
        }
        result.push({ label: label, textEdit: TextEdit.replace(range, JSON.stringify(label)) });
        return result;
    };
    return JSONDocumentSymbols;
}());
export { JSONDocumentSymbols };
//# sourceMappingURL=jsonDocumentSymbols.js.map