import { Bell, Search, UserCircle2 } from "lucide-react";

function Topbar() {
    return (
        <header className="h-16 bg-white border-b flex items-center justify-between px-6">
            <h2 className="text-xl font-semibold text-slate-800">
                Industrial Intelligence Platform
            </h2>

            <div className="flex items-center gap-4">
                <div className="flex items-center bg-slate-100 rounded-lg px-3 py-2">
                    <Search size={18} className="text-slate-500" />
                    <input
                        type="text"
                        placeholder="Search assets..."
                        className="bg-transparent outline-none ml-2 text-sm"
                    />
                </div>

                <Bell className="cursor-pointer text-slate-600" size={20} />
                <UserCircle2 className="cursor-pointer text-slate-600" size={28} />
            </div>
        </header>
    );
}

export default Topbar;