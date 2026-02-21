import { useState, useRef, useEffect } from "react"
import { api } from "@/lib/api"
import { SidebarTrigger } from "@/components/ui/sidebar"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Send, Loader2 } from "lucide-react"

type Message = { role: "user" | "assistant"; content: string }

export function ChatInterface({ activeCollection }: { activeCollection: string }) {
    const [messages, setMessages] = useState<Message[]>([])
    const [input, setInput] = useState("")
    const [loading, setLoading] = useState(false)
    const scrollRef = useRef<HTMLDivElement>(null)

    // Auto-scroll to bottom of chat
    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollIntoView({ behavior: "smooth" })
        }
    }, [messages])

    const handleSend = async (e?: React.FormEvent) => {
        e?.preventDefault()
        if (!input.trim() || !activeCollection) return

        const userMessage = input.trim()
        setInput("")
        setMessages(prev => [...prev, { role: "user", content: userMessage }])
        setLoading(true)

        try {
            const res = await api.chat(activeCollection, userMessage)
            setMessages(prev => [...prev, { role: "assistant", content: res.answer }])
        } catch (err) {
            console.error(err)
            setMessages(prev => [...prev, { role: "assistant", content: "Error: Could not retrieve answer." }])
        } finally {
            setLoading(false)
        }
    }

    return (
        <main className="flex w-full flex-col h-screen overflow-hidden">
            <header className="flex h-14 shrink-0 items-center justify-between border-b px-4">
                <div className="flex items-center gap-2">
                    <SidebarTrigger className="-ml-1" />
                    <h1 className="text-sm font-semibold">{activeCollection || "Select a collection to start chatting"}</h1>
                </div>
            </header>

            <div className="flex-1 overflow-hidden relative">
                <ScrollArea className="h-full w-full px-4 py-6">
                    <div className="flex flex-col gap-4 max-w-3xl mx-auto pb-20">
                        {messages.length === 0 && (
                            <div className="flex flex-col bg-muted/50 p-4 rounded-xl max-w-[80%] mr-auto">
                                <span className="text-sm font-semibold mb-1">AI Assistant</span>
                                <p className="text-sm">Hello! I'm ready to answer questions based on your documents. Select a collection or upload a new PDF to get started.</p>
                            </div>
                        )}

                        {messages.map((m, i) => (
                            <div key={i} className={`flex flex-col p-4 rounded-xl max-w-[80%] ${m.role === "user" ? "bg-primary text-primary-foreground ml-auto" : "bg-muted/50 mr-auto"}`}>
                                <span className="text-xs font-semibold mb-1 opacity-80">{m.role === "user" ? "You" : "AI Assistant"}</span>
                                <p className="text-sm whitespace-pre-wrap">{m.content}</p>
                            </div>
                        ))}
                        {loading && (
                            <div className="flex flex-col bg-muted/50 p-4 rounded-xl max-w-[80%] mr-auto">
                                <Loader2 className="h-4 w-4 animate-spin" />
                            </div>
                        )}
                        <div ref={scrollRef} />
                    </div>
                </ScrollArea>

                {/* Input Area */}
                <div className="absolute bottom-0 left-0 w-full bg-background/80 backdrop-blur-sm border-t p-4">
                    <form onSubmit={handleSend} className="max-w-3xl mx-auto flex gap-2">
                        <Input
                            placeholder="Ask a question about your documents..."
                            className="flex-1 shadow-sm"
                            value={input}
                            onChange={e => setInput(e.target.value)}
                            disabled={loading || !activeCollection}
                            autoComplete="off"
                        />
                        <Button size="icon" type="submit" disabled={loading || !activeCollection || !input.trim()}>
                            <Send className="h-4 w-4" />
                            <span className="sr-only">Send message</span>
                        </Button>
                    </form>
                </div>
            </div>
        </main>
    )
}
