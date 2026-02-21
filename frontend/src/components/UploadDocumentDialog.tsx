import { useState, useRef } from "react"
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
import { Label } from "@/components/ui/label"
import { Upload } from "lucide-react"
import { SidebarMenuButton } from "@/components/ui/sidebar"

export function UploadDocumentDialog({ activeCollection }: { activeCollection: string }) {
    const [open, setOpen] = useState(false)
    const [file, setFile] = useState<File | null>(null)
    const [loading, setLoading] = useState(false)
    const fileInputRef = useRef<HTMLInputElement>(null)

    const handleUpload = async () => {
        if (!file || !activeCollection) return;
        setLoading(true)
        try {
            await api.uploadDocument(activeCollection, file)
            setOpen(false)
            setFile(null)
        } catch (e) {
            console.error(e)
        } finally {
            setLoading(false)
        }
    }

    return (
        <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
                <SidebarMenuButton tooltip="Upload PDF" disabled={!activeCollection}>
                    <Upload />
                    <span>Upload PDF</span>
                </SidebarMenuButton>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle>Upload Document</DialogTitle>
                    <DialogDescription>
                        Upload a PDF document to the <strong>{activeCollection}</strong> collection.
                    </DialogDescription>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                    <div className="grid items-center gap-4">
                        <Label htmlFor="pdf_file">Select PDF File</Label>
                        <input
                            id="pdf_file"
                            type="file"
                            accept="application/pdf"
                            ref={fileInputRef}
                            onChange={(e) => setFile(e.target.files?.[0] || null)}
                            disabled={loading}
                            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                        />
                    </div>
                </div>
                <DialogFooter>
                    <Button onClick={handleUpload} disabled={loading || !file || !activeCollection}>
                        {loading ? "Uploading..." : "Upload"}
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
}
