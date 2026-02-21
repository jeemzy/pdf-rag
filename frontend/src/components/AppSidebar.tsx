import { useEffect, useState } from "react"
import { api } from "@/lib/api"
import {
    Sidebar,
    SidebarContent,
    SidebarGroup,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarHeader,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
} from "@/components/ui/sidebar"
import { Folder } from "lucide-react"
import { NewCollectionDialog } from "@/components/NewCollectionDialog"
import { UploadDocumentDialog } from "@/components/UploadDocumentDialog"

export function AppSidebar({ activeCollection, setActiveCollection }: { activeCollection: string, setActiveCollection: (c: string) => void }) {
    const [collections, setCollections] = useState<string[]>([])

    useEffect(() => {
        api.getCollections().then(setCollections).catch(console.error)
    }, [])

    return (
        <Sidebar>
            <SidebarHeader className="p-4">
                <h2 className="text-lg font-semibold tracking-tight">RAG App</h2>
            </SidebarHeader>
            <SidebarContent>
                {/* Collections Group */}
                <SidebarGroup>
                    <SidebarGroupLabel>Collections</SidebarGroupLabel>
                    <SidebarGroupContent>
                        <SidebarMenu>
                            <SidebarMenuItem>
                                <NewCollectionDialog onCreated={() => api.getCollections().then(setCollections).catch(console.error)} />
                            </SidebarMenuItem>
                            {collections.map(col => (
                                <SidebarMenuItem key={col}>
                                    <SidebarMenuButton
                                        isActive={activeCollection === col}
                                        onClick={() => setActiveCollection(col)}
                                    >
                                        <Folder />
                                        <span>{col}</span>
                                    </SidebarMenuButton>
                                </SidebarMenuItem>
                            ))}
                        </SidebarMenu>
                    </SidebarGroupContent>
                </SidebarGroup>

                {/* Documents Group */}
                <SidebarGroup>
                    <SidebarGroupLabel>Documents</SidebarGroupLabel>
                    <SidebarGroupContent>
                        <SidebarMenu>
                            <SidebarMenuItem>
                                <UploadDocumentDialog activeCollection={activeCollection} />
                            </SidebarMenuItem>
                        </SidebarMenu>
                    </SidebarGroupContent>
                </SidebarGroup>
            </SidebarContent>
        </Sidebar>
    )
}
