import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";

function Layout({ children }) {
    return (
        <div className="flex h-screen bg-slate-100">
            <Sidebar />

            <div className="flex flex-1 flex-col">
                <Topbar />

                <main className="flex-1 overflow-auto p-6">
                    {children}
                </main>
            </div>
        </div>
    );
}

export default Layout;