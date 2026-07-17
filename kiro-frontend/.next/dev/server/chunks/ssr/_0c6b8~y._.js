module.exports = [
"[project]/app/chat/page.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>ChatTest
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
"use client";
;
;
const BACKEND_URL = ("TURBOPACK compile-time value", "http://localhost:8000") || "https://kyroo-backend.onrender.com";
function ChatTest() {
    const [userId, setUserId] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    const [userName, setUserName] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])("");
    const [messages, setMessages] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])([]);
    const [input, setInput] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])("");
    const [sending, setSending] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(false);
    const [setupName, setSetupName] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])("");
    const [setupPhone, setSetupPhone] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])("");
    const [settingUp, setSettingUp] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(false);
    const [setupError, setSetupError] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])("");
    const [showEmojiPicker, setShowEmojiPicker] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(false);
    const [listening, setListening] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(false);
    const [voiceSupported, setVoiceSupported] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(false);
    const [pendingImage, setPendingImage] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    const bottomRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    const pendingRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])([]);
    const debounceTimerRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    const recognitionRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    const fileInputRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    const DEBOUNCE_MS = 1200;
    const EMOJI_OPTIONS = [
        "😭",
        "💀",
        "🔥",
        "😩",
        "🥲",
        "👀",
        "🙏",
        "😤",
        "💯",
        "🫡",
        "😂",
        "❤️",
        "💪",
        "😍",
        "🤔",
        "😅",
        "🙈",
        "✨",
        "🎉",
        "😴"
    ];
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        const savedId = localStorage.getItem("kyroo_test_user_id");
        const savedName = localStorage.getItem("kyroo_test_user_name");
        if (savedId) {
            setUserId(savedId);
            setUserName(savedName || "");
        }
    }, []);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) return;
        setVoiceSupported(true);
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "en-IN";
        recognition.onresult = (event)=>{
            const transcript = event.results[0][0].transcript;
            setInput((prev)=>prev ? `${prev} ${transcript}` : transcript);
        };
        recognition.onend = ()=>setListening(false);
        recognition.onerror = ()=>setListening(false);
        recognitionRef.current = recognition;
    }, []);
    const toggleVoiceInput = ()=>{
        if (!recognitionRef.current) return;
        if (listening) {
            recognitionRef.current.stop();
            setListening(false);
        } else {
            recognitionRef.current.start();
            setListening(true);
        }
    };
    const addEmoji = (emoji)=>{
        setInput((prev)=>prev + emoji);
        setShowEmojiPicker(false);
    };
    const handleImageSelect = (e)=>{
        const file = e.target.files?.[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = ()=>{
            const dataUrl = reader.result;
            const base64 = dataUrl.split(",")[1];
            setPendingImage({
                base64,
                mediaType: file.type || "image/jpeg",
                previewUrl: dataUrl
            });
        };
        reader.readAsDataURL(file);
        e.target.value = "";
    };
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        bottomRef.current?.scrollIntoView({
            behavior: "smooth"
        });
    }, [
        messages
    ]);
    const createTestUser = async ()=>{
        if (!setupName.trim() || !setupPhone.trim()) return;
        setSettingUp(true);
        setSetupError("");
        try {
            const res = await fetch(`${BACKEND_URL}/users/signup`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: setupName,
                    email: `${setupPhone}.${Date.now()}@kyroo.test`,
                    phone: setupPhone,
                    language: "Hinglish",
                    plan: "free"
                })
            });
            const data = await res.json();
            if (data.user_id) {
                localStorage.setItem("kyroo_test_user_id", data.user_id);
                localStorage.setItem("kyroo_test_user_name", setupName);
                setUserId(data.user_id);
                setUserName(setupName);
            } else {
                setSetupError(data.detail || "Something went wrong");
            }
        } catch  {
            setSetupError("Couldn't reach the backend. Is it running?");
        }
        setSettingUp(false);
    };
    const switchUser = ()=>{
        localStorage.removeItem("kyroo_test_user_id");
        localStorage.removeItem("kyroo_test_user_name");
        setUserId(null);
        setMessages([]);
    };
    // Debounces rapid consecutive sends into one combined message before
    // hitting the backend, mirroring how someone splits one thought across
    // 2-3 texts in real chat instead of writing it all in one message.
    const sendMessage = ()=>{
        const text = input.trim();
        if (!userId) return;
        // an attached image sends immediately with the current text as caption,
        // bypassing the multi-message debounce (images aren't meant to be batched)
        if (pendingImage) {
            const image = pendingImage;
            setInput("");
            setPendingImage(null);
            setMessages((m)=>[
                    ...m,
                    {
                        role: "user",
                        text,
                        imagePreview: image.previewUrl
                    }
                ]);
            dispatchToBackend(text, image);
            return;
        }
        if (!text) return;
        setInput("");
        setMessages((m)=>[
                ...m,
                {
                    role: "user",
                    text
                }
            ]);
        pendingRef.current.push(text);
        if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);
        debounceTimerRef.current = setTimeout(()=>{
            const combined = pendingRef.current.join("\n");
            pendingRef.current = [];
            debounceTimerRef.current = null;
            dispatchToBackend(combined);
        }, DEBOUNCE_MS);
    };
    const dispatchToBackend = async (text, image)=>{
        setSending(true);
        try {
            const res = await fetch(`${BACKEND_URL}/ai/chat`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    user_id: userId,
                    message: text,
                    ...image ? {
                        image_base64: image.base64,
                        image_media_type: image.mediaType
                    } : {}
                })
            });
            const data = await res.json();
            const bubbles = data.bubbles && data.bubbles.length ? data.bubbles : [
                data.response || "(no response)"
            ];
            for(let i = 0; i < bubbles.length; i++){
                if (i > 0) {
                    setSending(true);
                    await new Promise((r)=>setTimeout(r, 350 + Math.random() * 450));
                }
                setMessages((m)=>[
                        ...m,
                        {
                            role: "kyroo",
                            text: bubbles[i],
                            module: i === bubbles.length - 1 ? data.module : undefined
                        }
                    ]);
            }
        } catch  {
            setMessages((m)=>[
                    ...m,
                    {
                        role: "kyroo",
                        text: "⚠️ Couldn't reach KYROO's backend. Check it's running on :8000."
                    }
                ]);
        }
        setSending(false);
    };
    const s = {
        background: "#0a0a0a",
        minHeight: "100vh",
        color: "#f0ede8",
        fontFamily: "sans-serif",
        display: "flex",
        flexDirection: "column"
    };
    const inputStyle = {
        width: "100%",
        background: "#111",
        border: "0.5px solid rgba(240,237,232,0.1)",
        borderRadius: 14,
        padding: "13px 16px",
        fontSize: 15,
        color: "#f0ede8",
        fontFamily: "sans-serif",
        outline: "none",
        marginBottom: 12
    };
    if (!userId) {
        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            style: {
                ...s,
                alignItems: "center",
                justifyContent: "center",
                padding: 24
            },
            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                style: {
                    width: "100%",
                    maxWidth: 380
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        style: {
                            textAlign: "center",
                            marginBottom: 28
                        },
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    fontSize: 20,
                                    fontWeight: 800,
                                    marginBottom: 6
                                },
                                children: [
                                    "KY",
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                        style: {
                                            color: "#c8f060"
                                        },
                                        children: "R"
                                    }, void 0, false, {
                                        fileName: "[project]/app/chat/page.tsx",
                                        lineNumber: 240,
                                        columnNumber: 17
                                    }, this),
                                    "OO test chat"
                                ]
                            }, void 0, true, {
                                fileName: "[project]/app/chat/page.tsx",
                                lineNumber: 239,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    fontSize: 13,
                                    color: "rgba(240,237,232,0.4)"
                                },
                                children: "Talk to KYROO directly in the browser — no WhatsApp needed. This hits the same AI brain that'll power WhatsApp once it's live."
                            }, void 0, false, {
                                fileName: "[project]/app/chat/page.tsx",
                                lineNumber: 242,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/app/chat/page.tsx",
                        lineNumber: 238,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                        style: {
                            fontSize: 11,
                            color: "rgba(240,237,232,0.35)",
                            display: "block",
                            marginBottom: 7
                        },
                        children: "Test name"
                    }, void 0, false, {
                        fileName: "[project]/app/chat/page.tsx",
                        lineNumber: 246,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                        style: inputStyle,
                        placeholder: "Aarya",
                        value: setupName,
                        onChange: (e)=>setSetupName(e.target.value)
                    }, void 0, false, {
                        fileName: "[project]/app/chat/page.tsx",
                        lineNumber: 249,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                        style: {
                            fontSize: 11,
                            color: "rgba(240,237,232,0.35)",
                            display: "block",
                            marginBottom: 7
                        },
                        children: "Any phone number (doesn't need to be real for this test mode)"
                    }, void 0, false, {
                        fileName: "[project]/app/chat/page.tsx",
                        lineNumber: 255,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                        style: inputStyle,
                        placeholder: "9876543210",
                        value: setupPhone,
                        onChange: (e)=>setSetupPhone(e.target.value)
                    }, void 0, false, {
                        fileName: "[project]/app/chat/page.tsx",
                        lineNumber: 258,
                        columnNumber: 11
                    }, this),
                    setupError && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        style: {
                            color: "#ff6b6b",
                            fontSize: 12,
                            marginBottom: 12
                        },
                        children: setupError
                    }, void 0, false, {
                        fileName: "[project]/app/chat/page.tsx",
                        lineNumber: 265,
                        columnNumber: 13
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        onClick: createTestUser,
                        disabled: settingUp || !setupName.trim() || !setupPhone.trim(),
                        style: {
                            width: "100%",
                            height: 50,
                            borderRadius: 14,
                            background: "#c8f060",
                            color: "#0a0a0a",
                            border: "none",
                            fontSize: 15,
                            fontWeight: 500,
                            cursor: "pointer",
                            fontFamily: "sans-serif",
                            opacity: settingUp ? 0.7 : 1
                        },
                        children: settingUp ? "Setting up..." : "Start chatting →"
                    }, void 0, false, {
                        fileName: "[project]/app/chat/page.tsx",
                        lineNumber: 267,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/app/chat/page.tsx",
                lineNumber: 237,
                columnNumber: 9
            }, this)
        }, void 0, false, {
            fileName: "[project]/app/chat/page.tsx",
            lineNumber: 236,
            columnNumber: 7
        }, this);
    }
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        style: s,
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                style: {
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    padding: "16px 20px",
                    borderBottom: "0.5px solid rgba(240,237,232,0.07)"
                },
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        style: {
                            display: "flex",
                            alignItems: "center",
                            gap: 10
                        },
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    width: 34,
                                    height: 34,
                                    borderRadius: "50%",
                                    background: "#c8f060",
                                    display: "flex",
                                    alignItems: "center",
                                    justifyContent: "center",
                                    fontWeight: 800,
                                    color: "#0a0a0a",
                                    fontSize: 13
                                },
                                children: "K"
                            }, void 0, false, {
                                fileName: "[project]/app/chat/page.tsx",
                                lineNumber: 303,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        style: {
                                            fontSize: 14,
                                            fontWeight: 600
                                        },
                                        children: "KYROO"
                                    }, void 0, false, {
                                        fileName: "[project]/app/chat/page.tsx",
                                        lineNumber: 320,
                                        columnNumber: 13
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        style: {
                                            fontSize: 11,
                                            color: "rgba(240,237,232,0.35)"
                                        },
                                        children: [
                                            "testing as ",
                                            userName
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/app/chat/page.tsx",
                                        lineNumber: 321,
                                        columnNumber: 13
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/app/chat/page.tsx",
                                lineNumber: 319,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/app/chat/page.tsx",
                        lineNumber: 302,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                        onClick: switchUser,
                        style: {
                            background: "transparent",
                            border: "0.5px solid rgba(240,237,232,0.15)",
                            borderRadius: 100,
                            padding: "7px 14px",
                            fontSize: 12,
                            color: "rgba(240,237,232,0.5)",
                            cursor: "pointer",
                            fontFamily: "sans-serif"
                        },
                        children: "Switch user"
                    }, void 0, false, {
                        fileName: "[project]/app/chat/page.tsx",
                        lineNumber: 326,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/app/chat/page.tsx",
                lineNumber: 293,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                style: {
                    flex: 1,
                    overflowY: "auto",
                    padding: "20px 16px"
                },
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    style: {
                        maxWidth: 560,
                        margin: "0 auto"
                    },
                    children: [
                        messages.length === 0 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            style: {
                                textAlign: "center",
                                color: "rgba(240,237,232,0.3)",
                                fontSize: 13,
                                marginTop: 40
                            },
                            children: "Say hi to KYROO — try Hinglish, Gen-Z slang, or plain English and see how it adapts."
                        }, void 0, false, {
                            fileName: "[project]/app/chat/page.tsx",
                            lineNumber: 346,
                            columnNumber: 13
                        }, this),
                        messages.map((m, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    display: "flex",
                                    justifyContent: m.role === "user" ? "flex-end" : "flex-start",
                                    marginBottom: 10
                                },
                                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    style: {
                                        maxWidth: "78%",
                                        padding: m.imagePreview ? 6 : "11px 15px",
                                        borderRadius: 16,
                                        borderBottomRightRadius: m.role === "user" ? 4 : 16,
                                        borderBottomLeftRadius: m.role === "kyroo" ? 4 : 16,
                                        background: m.role === "user" ? "#c8f060" : "#161616",
                                        color: m.role === "user" ? "#0a0a0a" : "#f0ede8",
                                        fontSize: 14,
                                        lineHeight: 1.5,
                                        whiteSpace: "pre-wrap"
                                    },
                                    children: [
                                        m.imagePreview && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("img", {
                                            src: m.imagePreview,
                                            alt: "sent",
                                            style: {
                                                maxWidth: "100%",
                                                borderRadius: 12,
                                                display: "block",
                                                marginBottom: m.text ? 6 : 0
                                            }
                                        }, void 0, false, {
                                            fileName: "[project]/app/chat/page.tsx",
                                            lineNumber: 381,
                                            columnNumber: 19
                                        }, this),
                                        m.text && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                            style: {
                                                padding: m.imagePreview ? "0 8px 6px" : 0
                                            },
                                            children: m.text
                                        }, void 0, false, {
                                            fileName: "[project]/app/chat/page.tsx",
                                            lineNumber: 392,
                                            columnNumber: 28
                                        }, this)
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/app/chat/page.tsx",
                                    lineNumber: 366,
                                    columnNumber: 15
                                }, this)
                            }, i, false, {
                                fileName: "[project]/app/chat/page.tsx",
                                lineNumber: 358,
                                columnNumber: 13
                            }, this)),
                        sending && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            style: {
                                display: "flex",
                                justifyContent: "flex-start",
                                marginBottom: 10
                            },
                            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    padding: "11px 15px",
                                    borderRadius: 16,
                                    borderBottomLeftRadius: 4,
                                    background: "#161616",
                                    color: "rgba(240,237,232,0.4)",
                                    fontSize: 14
                                },
                                children: "KYROO is typing..."
                            }, void 0, false, {
                                fileName: "[project]/app/chat/page.tsx",
                                lineNumber: 398,
                                columnNumber: 15
                            }, this)
                        }, void 0, false, {
                            fileName: "[project]/app/chat/page.tsx",
                            lineNumber: 397,
                            columnNumber: 13
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            ref: bottomRef
                        }, void 0, false, {
                            fileName: "[project]/app/chat/page.tsx",
                            lineNumber: 412,
                            columnNumber: 11
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/app/chat/page.tsx",
                    lineNumber: 344,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/app/chat/page.tsx",
                lineNumber: 343,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                style: {
                    padding: "14px 16px",
                    borderTop: "0.5px solid rgba(240,237,232,0.06)",
                    position: "relative"
                },
                children: [
                    showEmojiPicker && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        style: {
                            position: "absolute",
                            bottom: "100%",
                            left: "50%",
                            transform: "translateX(-50%)",
                            marginBottom: 8,
                            background: "#161616",
                            border: "0.5px solid rgba(240,237,232,0.1)",
                            borderRadius: 14,
                            padding: 10,
                            display: "grid",
                            gridTemplateColumns: "repeat(5, 1fr)",
                            gap: 4,
                            maxWidth: 560,
                            width: "calc(100% - 32px)",
                            boxShadow: "0 8px 24px rgba(0,0,0,0.4)"
                        },
                        children: EMOJI_OPTIONS.map((emoji)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                onClick: ()=>addEmoji(emoji),
                                style: {
                                    background: "transparent",
                                    border: "none",
                                    fontSize: 22,
                                    padding: 8,
                                    cursor: "pointer",
                                    borderRadius: 8
                                },
                                children: emoji
                            }, emoji, false, {
                                fileName: "[project]/app/chat/page.tsx",
                                lineNumber: 444,
                                columnNumber: 15
                            }, this))
                    }, void 0, false, {
                        fileName: "[project]/app/chat/page.tsx",
                        lineNumber: 424,
                        columnNumber: 11
                    }, this),
                    pendingImage && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        style: {
                            maxWidth: 560,
                            margin: "0 auto 10px",
                            display: "flex",
                            alignItems: "center",
                            gap: 10
                        },
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                style: {
                                    position: "relative"
                                },
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("img", {
                                        src: pendingImage.previewUrl,
                                        alt: "preview",
                                        style: {
                                            height: 56,
                                            width: 56,
                                            objectFit: "cover",
                                            borderRadius: 10
                                        }
                                    }, void 0, false, {
                                        fileName: "[project]/app/chat/page.tsx",
                                        lineNumber: 472,
                                        columnNumber: 15
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        onClick: ()=>setPendingImage(null),
                                        style: {
                                            position: "absolute",
                                            top: -6,
                                            right: -6,
                                            width: 20,
                                            height: 20,
                                            borderRadius: "50%",
                                            background: "#ff5050",
                                            color: "#fff",
                                            border: "none",
                                            fontSize: 12,
                                            cursor: "pointer",
                                            lineHeight: "20px"
                                        },
                                        type: "button",
                                        children: "×"
                                    }, void 0, false, {
                                        fileName: "[project]/app/chat/page.tsx",
                                        lineNumber: 477,
                                        columnNumber: 15
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/app/chat/page.tsx",
                                lineNumber: 471,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                style: {
                                    fontSize: 12,
                                    color: "rgba(240,237,232,0.4)"
                                },
                                children: "Add a caption or just hit send"
                            }, void 0, false, {
                                fileName: "[project]/app/chat/page.tsx",
                                lineNumber: 498,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/app/chat/page.tsx",
                        lineNumber: 462,
                        columnNumber: 11
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        style: {
                            maxWidth: 560,
                            margin: "0 auto",
                            display: "flex",
                            gap: 8
                        },
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                                ref: fileInputRef,
                                type: "file",
                                accept: "image/*",
                                style: {
                                    display: "none"
                                },
                                onChange: handleImageSelect
                            }, void 0, false, {
                                fileName: "[project]/app/chat/page.tsx",
                                lineNumber: 504,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                onClick: ()=>fileInputRef.current?.click(),
                                style: {
                                    width: 44,
                                    height: 50,
                                    borderRadius: 14,
                                    background: pendingImage ? "rgba(200,240,96,0.15)" : "transparent",
                                    border: "0.5px solid rgba(240,237,232,0.12)",
                                    color: "#f0ede8",
                                    fontSize: 18,
                                    cursor: "pointer",
                                    flexShrink: 0
                                },
                                type: "button",
                                children: "📷"
                            }, void 0, false, {
                                fileName: "[project]/app/chat/page.tsx",
                                lineNumber: 511,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                onClick: ()=>setShowEmojiPicker((v)=>!v),
                                style: {
                                    width: 44,
                                    height: 50,
                                    borderRadius: 14,
                                    background: showEmojiPicker ? "rgba(200,240,96,0.15)" : "transparent",
                                    border: "0.5px solid rgba(240,237,232,0.12)",
                                    color: "#f0ede8",
                                    fontSize: 18,
                                    cursor: "pointer",
                                    flexShrink: 0
                                },
                                type: "button",
                                children: "😊"
                            }, void 0, false, {
                                fileName: "[project]/app/chat/page.tsx",
                                lineNumber: 528,
                                columnNumber: 11
                            }, this),
                            voiceSupported && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                onClick: toggleVoiceInput,
                                style: {
                                    width: 44,
                                    height: 50,
                                    borderRadius: 14,
                                    background: listening ? "rgba(255,80,80,0.15)" : "transparent",
                                    border: listening ? "0.5px solid rgba(255,80,80,0.4)" : "0.5px solid rgba(240,237,232,0.12)",
                                    color: listening ? "#ff5050" : "#f0ede8",
                                    fontSize: 18,
                                    cursor: "pointer",
                                    flexShrink: 0
                                },
                                type: "button",
                                children: listening ? "⏹" : "🎙"
                            }, void 0, false, {
                                fileName: "[project]/app/chat/page.tsx",
                                lineNumber: 546,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("textarea", {
                                style: {
                                    ...inputStyle,
                                    marginBottom: 0,
                                    flex: 1,
                                    resize: "none",
                                    maxHeight: 120,
                                    fontFamily: "sans-serif"
                                },
                                placeholder: "Type a message... (Shift+Enter for new line)",
                                value: input,
                                rows: Math.min(5, input.split("\n").length),
                                onChange: (e)=>setInput(e.target.value),
                                onKeyDown: (e)=>{
                                    if (e.key === "Enter" && !e.shiftKey) {
                                        e.preventDefault();
                                        sendMessage();
                                    }
                                }
                            }, void 0, false, {
                                fileName: "[project]/app/chat/page.tsx",
                                lineNumber: 564,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                onClick: sendMessage,
                                disabled: !input.trim() && !pendingImage,
                                style: {
                                    width: 50,
                                    height: 50,
                                    borderRadius: 14,
                                    background: "#c8f060",
                                    color: "#0a0a0a",
                                    border: "none",
                                    fontSize: 18,
                                    cursor: "pointer",
                                    flexShrink: 0,
                                    opacity: !input.trim() && !pendingImage ? 0.5 : 1
                                },
                                children: "→"
                            }, void 0, false, {
                                fileName: "[project]/app/chat/page.tsx",
                                lineNumber: 584,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/app/chat/page.tsx",
                        lineNumber: 503,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/app/chat/page.tsx",
                lineNumber: 416,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/app/chat/page.tsx",
        lineNumber: 292,
        columnNumber: 5
    }, this);
}
}),
"[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

module.exports = __turbopack_context__.r("[project]/node_modules/next/dist/server/route-modules/app-page/module.compiled.js [app-ssr] (ecmascript)").vendored['react-ssr'].ReactJsxDevRuntime;
}),
];

//# sourceMappingURL=_0c6b8~y._.js.map