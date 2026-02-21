import { useState } from "react"
import { SidebarProvider } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/AppSidebar"
import { ChatInterface } from "@/components/ChatInterface"
import { TooltipProvider } from "@/components/ui/tooltip"

export function App() {
    const [activeCollection, setActiveCollection] = useState<string>("");

    return (
        <TooltipProvider>
            <SidebarProvider>
                <div className="flex w-full h-screen bg-background text-foreground overflow-hidden">
                    <AppSidebar activeCollection={activeCollection} setActiveCollection={setActiveCollection} />
                    <ChatInterface activeCollection={activeCollection} />
                </div>
            </SidebarProvider>
        </TooltipProvider>
    )
}

export default App;