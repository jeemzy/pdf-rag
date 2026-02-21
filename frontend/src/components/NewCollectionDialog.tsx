import { useState } from "react"
import { api } from "@/lib/api"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Plus } from "lucide-react"
import { SidebarMenuButton } from "@/components/ui/sidebar"

export function NewCollectionDialog({ onCreated }: { onCreated: () => void }) {
    const [open, setOpen] = useState(false)
    const [name, setName] = useState("")
    const [loading, setLoading] = useState(false)

    const handleCreate = async () => {
        if (!name.trim()) return;
        setLoading(true)
        try {
            await api.createCollection(name.trim())
            onCreated()
            setOpen(false)
            setName("")
        } catch (e) {
            console.error(e)
        } finally {
            setLoading(false)
        }
    }

    return (
        <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
                <SidebarMenuButton tooltip="New Collection">
                    <Plus />
                    <span>New Collection</span>
                </SidebarMenuButton>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle>Create New Collection</DialogTitle>
                    <DialogDescription>
                        Enter a unique name for your new document collection.
                    </DialogDescription>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                    <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="name" className="text-right">
                            Name
                        </Label>
                        <Input
                            id="name"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            className="col-span-3"
                            disabled={loading}
                            autoComplete="off"
                        />
                    </div>
                </div>
                <DialogFooter>
                    <Button onClick={handleCreate} disabled={loading || !name.trim()}>Create</Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
}
