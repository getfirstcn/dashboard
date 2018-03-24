/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/
'use strict';
import { KeyCodeUtils, SimpleKeybinding } from '../common/keyCodes.js';
import * as platform from '../common/platform.js';
import * as browser from './browser.js';
var KEY_CODE_MAP = {};
(function () {
    KEY_CODE_MAP[3] = 7 /* PauseBreak */; // VK_CANCEL 0x03 Control-break processing
    KEY_CODE_MAP[8] = 1 /* Backspace */;
    KEY_CODE_MAP[9] = 2 /* Tab */;
    KEY_CODE_MAP[13] = 3 /* Enter */;
    KEY_CODE_MAP[16] = 4 /* Shift */;
    KEY_CODE_MAP[17] = 5 /* Ctrl */;
    KEY_CODE_MAP[18] = 6 /* Alt */;
    KEY_CODE_MAP[19] = 7 /* PauseBreak */;
    KEY_CODE_MAP[20] = 8 /* CapsLock */;
    KEY_CODE_MAP[27] = 9 /* Escape */;
    KEY_CODE_MAP[32] = 10 /* Space */;
    KEY_CODE_MAP[33] = 11 /* PageUp */;
    KEY_CODE_MAP[34] = 12 /* PageDown */;
    KEY_CODE_MAP[35] = 13 /* End */;
    KEY_CODE_MAP[36] = 14 /* Home */;
    KEY_CODE_MAP[37] = 15 /* LeftArrow */;
    KEY_CODE_MAP[38] = 16 /* UpArrow */;
    KEY_CODE_MAP[39] = 17 /* RightArrow */;
    KEY_CODE_MAP[40] = 18 /* DownArrow */;
    KEY_CODE_MAP[45] = 19 /* Insert */;
    KEY_CODE_MAP[46] = 20 /* Delete */;
    KEY_CODE_MAP[48] = 21 /* KEY_0 */;
    KEY_CODE_MAP[49] = 22 /* KEY_1 */;
    KEY_CODE_MAP[50] = 23 /* KEY_2 */;
    KEY_CODE_MAP[51] = 24 /* KEY_3 */;
    KEY_CODE_MAP[52] = 25 /* KEY_4 */;
    KEY_CODE_MAP[53] = 26 /* KEY_5 */;
    KEY_CODE_MAP[54] = 27 /* KEY_6 */;
    KEY_CODE_MAP[55] = 28 /* KEY_7 */;
    KEY_CODE_MAP[56] = 29 /* KEY_8 */;
    KEY_CODE_MAP[57] = 30 /* KEY_9 */;
    KEY_CODE_MAP[65] = 31 /* KEY_A */;
    KEY_CODE_MAP[66] = 32 /* KEY_B */;
    KEY_CODE_MAP[67] = 33 /* KEY_C */;
    KEY_CODE_MAP[68] = 34 /* KEY_D */;
    KEY_CODE_MAP[69] = 35 /* KEY_E */;
    KEY_CODE_MAP[70] = 36 /* KEY_F */;
    KEY_CODE_MAP[71] = 37 /* KEY_G */;
    KEY_CODE_MAP[72] = 38 /* KEY_H */;
    KEY_CODE_MAP[73] = 39 /* KEY_I */;
    KEY_CODE_MAP[74] = 40 /* KEY_J */;
    KEY_CODE_MAP[75] = 41 /* KEY_K */;
    KEY_CODE_MAP[76] = 42 /* KEY_L */;
    KEY_CODE_MAP[77] = 43 /* KEY_M */;
    KEY_CODE_MAP[78] = 44 /* KEY_N */;
    KEY_CODE_MAP[79] = 45 /* KEY_O */;
    KEY_CODE_MAP[80] = 46 /* KEY_P */;
    KEY_CODE_MAP[81] = 47 /* KEY_Q */;
    KEY_CODE_MAP[82] = 48 /* KEY_R */;
    KEY_CODE_MAP[83] = 49 /* KEY_S */;
    KEY_CODE_MAP[84] = 50 /* KEY_T */;
    KEY_CODE_MAP[85] = 51 /* KEY_U */;
    KEY_CODE_MAP[86] = 52 /* KEY_V */;
    KEY_CODE_MAP[87] = 53 /* KEY_W */;
    KEY_CODE_MAP[88] = 54 /* KEY_X */;
    KEY_CODE_MAP[89] = 55 /* KEY_Y */;
    KEY_CODE_MAP[90] = 56 /* KEY_Z */;
    KEY_CODE_MAP[93] = 58 /* ContextMenu */;
    KEY_CODE_MAP[96] = 93 /* NUMPAD_0 */;
    KEY_CODE_MAP[97] = 94 /* NUMPAD_1 */;
    KEY_CODE_MAP[98] = 95 /* NUMPAD_2 */;
    KEY_CODE_MAP[99] = 96 /* NUMPAD_3 */;
    KEY_CODE_MAP[100] = 97 /* NUMPAD_4 */;
    KEY_CODE_MAP[101] = 98 /* NUMPAD_5 */;
    KEY_CODE_MAP[102] = 99 /* NUMPAD_6 */;
    KEY_CODE_MAP[103] = 100 /* NUMPAD_7 */;
    KEY_CODE_MAP[104] = 101 /* NUMPAD_8 */;
    KEY_CODE_MAP[105] = 102 /* NUMPAD_9 */;
    KEY_CODE_MAP[106] = 103 /* NUMPAD_MULTIPLY */;
    KEY_CODE_MAP[107] = 104 /* NUMPAD_ADD */;
    KEY_CODE_MAP[108] = 105 /* NUMPAD_SEPARATOR */;
    KEY_CODE_MAP[109] = 106 /* NUMPAD_SUBTRACT */;
    KEY_CODE_MAP[110] = 107 /* NUMPAD_DECIMAL */;
    KEY_CODE_MAP[111] = 108 /* NUMPAD_DIVIDE */;
    KEY_CODE_MAP[112] = 59 /* F1 */;
    KEY_CODE_MAP[113] = 60 /* F2 */;
    KEY_CODE_MAP[114] = 61 /* F3 */;
    KEY_CODE_MAP[115] = 62 /* F4 */;
    KEY_CODE_MAP[116] = 63 /* F5 */;
    KEY_CODE_MAP[117] = 64 /* F6 */;
    KEY_CODE_MAP[118] = 65 /* F7 */;
    KEY_CODE_MAP[119] = 66 /* F8 */;
    KEY_CODE_MAP[120] = 67 /* F9 */;
    KEY_CODE_MAP[121] = 68 /* F10 */;
    KEY_CODE_MAP[122] = 69 /* F11 */;
    KEY_CODE_MAP[123] = 70 /* F12 */;
    KEY_CODE_MAP[124] = 71 /* F13 */;
    KEY_CODE_MAP[125] = 72 /* F14 */;
    KEY_CODE_MAP[126] = 73 /* F15 */;
    KEY_CODE_MAP[127] = 74 /* F16 */;
    KEY_CODE_MAP[128] = 75 /* F17 */;
    KEY_CODE_MAP[129] = 76 /* F18 */;
    KEY_CODE_MAP[130] = 77 /* F19 */;
    KEY_CODE_MAP[144] = 78 /* NumLock */;
    KEY_CODE_MAP[145] = 79 /* ScrollLock */;
    KEY_CODE_MAP[186] = 80 /* US_SEMICOLON */;
    KEY_CODE_MAP[187] = 81 /* US_EQUAL */;
    KEY_CODE_MAP[188] = 82 /* US_COMMA */;
    KEY_CODE_MAP[189] = 83 /* US_MINUS */;
    KEY_CODE_MAP[190] = 84 /* US_DOT */;
    KEY_CODE_MAP[191] = 85 /* US_SLASH */;
    KEY_CODE_MAP[192] = 86 /* US_BACKTICK */;
    KEY_CODE_MAP[193] = 110 /* ABNT_C1 */;
    KEY_CODE_MAP[194] = 111 /* ABNT_C2 */;
    KEY_CODE_MAP[219] = 87 /* US_OPEN_SQUARE_BRACKET */;
    KEY_CODE_MAP[220] = 88 /* US_BACKSLASH */;
    KEY_CODE_MAP[221] = 89 /* US_CLOSE_SQUARE_BRACKET */;
    KEY_CODE_MAP[222] = 90 /* US_QUOTE */;
    KEY_CODE_MAP[223] = 91 /* OEM_8 */;
    KEY_CODE_MAP[226] = 92 /* OEM_102 */;
    /**
     * https://lists.w3.org/Archives/Public/www-dom/2010JulSep/att-0182/keyCode-spec.html
     * If an Input Method Editor is processing key input and the event is keydown, return 229.
     */
    KEY_CODE_MAP[229] = 109 /* KEY_IN_COMPOSITION */;
    if (browser.isIE) {
        KEY_CODE_MAP[91] = 57 /* Meta */;
    }
    else if (browser.isFirefox) {
        KEY_CODE_MAP[59] = 80 /* US_SEMICOLON */;
        KEY_CODE_MAP[107] = 81 /* US_EQUAL */;
        KEY_CODE_MAP[109] = 83 /* US_MINUS */;
        if (platform.isMacintosh) {
            KEY_CODE_MAP[224] = 57 /* Meta */;
        }
    }
    else if (browser.isWebKit) {
        KEY_CODE_MAP[91] = 57 /* Meta */;
        if (platform.isMacintosh) {
            // the two meta keys in the Mac have different key codes (91 and 93)
            KEY_CODE_MAP[93] = 57 /* Meta */;
        }
        else {
            KEY_CODE_MAP[92] = 57 /* Meta */;
        }
    }
})();
function extractKeyCode(e) {
    if (e.charCode) {
        // "keypress" events mostly
        var char = String.fromCharCode(e.charCode).toUpperCase();
        return KeyCodeUtils.fromString(char);
    }
    return KEY_CODE_MAP[e.keyCode] || 0 /* Unknown */;
}
var ctrlKeyMod = (platform.isMacintosh ? 256 /* WinCtrl */ : 2048 /* CtrlCmd */);
var altKeyMod = 512 /* Alt */;
var shiftKeyMod = 1024 /* Shift */;
var metaKeyMod = (platform.isMacintosh ? 2048 /* CtrlCmd */ : 256 /* WinCtrl */);
var StandardKeyboardEvent = /** @class */ (function () {
    function StandardKeyboardEvent(source) {
        var e = source;
        this.browserEvent = e;
        this.target = e.target;
        this.ctrlKey = e.ctrlKey;
        this.shiftKey = e.shiftKey;
        this.altKey = e.altKey;
        this.metaKey = e.metaKey;
        this.keyCode = extractKeyCode(e);
        this.code = e.code;
        // console.info(e.type + ": keyCode: " + e.keyCode + ", which: " + e.which + ", charCode: " + e.charCode + ", detail: " + e.detail + " ====> " + this.keyCode + ' -- ' + KeyCode[this.keyCode]);
        this.ctrlKey = this.ctrlKey || this.keyCode === 5 /* Ctrl */;
        this.altKey = this.altKey || this.keyCode === 6 /* Alt */;
        this.shiftKey = this.shiftKey || this.keyCode === 4 /* Shift */;
        this.metaKey = this.metaKey || this.keyCode === 57 /* Meta */;
        this._asKeybinding = this._computeKeybinding();
        this._asRuntimeKeybinding = this._computeRuntimeKeybinding();
        // console.log(`code: ${e.code}, keyCode: ${e.keyCode}, key: ${e.key}`);
    }
    StandardKeyboardEvent.prototype.preventDefault = function () {
        if (this.browserEvent && this.browserEvent.preventDefault) {
            this.browserEvent.preventDefault();
        }
    };
    StandardKeyboardEvent.prototype.stopPropagation = function () {
        if (this.browserEvent && this.browserEvent.stopPropagation) {
            this.browserEvent.stopPropagation();
        }
    };
    StandardKeyboardEvent.prototype.toKeybinding = function () {
        return this._asRuntimeKeybinding;
    };
    StandardKeyboardEvent.prototype.equals = function (other) {
        return this._asKeybinding === other;
    };
    StandardKeyboardEvent.prototype._computeKeybinding = function () {
        var key = 0 /* Unknown */;
        if (this.keyCode !== 5 /* Ctrl */ && this.keyCode !== 4 /* Shift */ && this.keyCode !== 6 /* Alt */ && this.keyCode !== 57 /* Meta */) {
            key = this.keyCode;
        }
        var result = 0;
        if (this.ctrlKey) {
            result |= ctrlKeyMod;
        }
        if (this.altKey) {
            result |= altKeyMod;
        }
        if (this.shiftKey) {
            result |= shiftKeyMod;
        }
        if (this.metaKey) {
            result |= metaKeyMod;
        }
        result |= key;
        return result;
    };
    StandardKeyboardEvent.prototype._computeRuntimeKeybinding = function () {
        var key = 0 /* Unknown */;
        if (this.keyCode !== 5 /* Ctrl */ && this.keyCode !== 4 /* Shift */ && this.keyCode !== 6 /* Alt */ && this.keyCode !== 57 /* Meta */) {
            key = this.keyCode;
        }
        return new SimpleKeybinding(this.ctrlKey, this.shiftKey, this.altKey, this.metaKey, key);
    };
    return StandardKeyboardEvent;
}());
export { StandardKeyboardEvent };
