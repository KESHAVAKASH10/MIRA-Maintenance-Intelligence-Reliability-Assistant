import {
    LayoutDashboard,
    Boxes,
    FolderOpen,
    Bot,
    ShieldCheck,
} from "lucide-react";

import { ROUTES } from "./routes";

export const NAVIGATION = [
    {
        name: "Dashboard",
        path: ROUTES.DASHBOARD,
        icon: LayoutDashboard,
    },
    {
        name: "Assets",
        path: ROUTES.ASSETS,
        icon: Boxes,
    },
    {
        name: "Documents",
        path: ROUTES.DOCUMENTS,
        icon: FolderOpen,
    },
    {
        name: "Industrial Copilot",
        path: ROUTES.COPILOT,
        icon: Bot,
    },
    {
        name: "Compliance",
        path: ROUTES.COMPLIANCE,
        icon: ShieldCheck,
    },
];