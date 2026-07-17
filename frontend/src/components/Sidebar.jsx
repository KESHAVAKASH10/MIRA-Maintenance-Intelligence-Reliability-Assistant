import { NavLink } from "react-router-dom";
import { NAVIGATION } from "../constants/navigation";

function Sidebar() {
    return (
        <aside className="w-64 bg-slate-900 text-white flex flex-col">
            <div className="p-6 border-b border-slate-700">
                <h1 className="text-2xl font-bold">MIRA</h1>
                <p className="text-sm text-slate-400 mt-1">
                    Maintenance Intelligence
                </p>
            </div>

            <nav className="flex-1 p-4">
                {NAVIGATION.map((item) => {
                    const Icon = item.icon;

                    return (
                        <NavLink
                            key={item.name}
                            to={item.path}
                            className={({ isActive }) =>
                                `flex items-center gap-3 rounded-lg px-4 py-3 mb-2 transition-all ${isActive
                                    ? "bg-blue-600 text-white"
                                    : "text-slate-300 hover:bg-slate-800 hover:text-white"
                                }`
                            }
                        >
                            <Icon size={20} />
                            <span>{item.name}</span>
                        </NavLink>
                    );
                })}
            </nav>

            <div className="p-4 border-t border-slate-700 text-xs text-slate-400">
                MIRA v1.0
            </div>
        </aside>
    );
}

export default Sidebar;