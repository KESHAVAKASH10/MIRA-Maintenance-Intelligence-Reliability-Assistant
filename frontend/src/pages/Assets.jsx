import PageHeader from "../components/PageHeader";
import SearchBar from "../components/SearchBar";
import AssetSummaryCard from "../components/AssetSummaryCard";

import { assetData } from "../data/assetData";

function Assets() {
    return (
        <>
            <PageHeader
                title="Asset Registry"
                subtitle="Browse and monitor industrial assets"
            />

            <div className="mb-8">
                <SearchBar placeholder="Search assets..." />
            </div>

            <div className="grid grid-cols-2 gap-6">
                {assetData.map((asset) => (
                    <AssetSummaryCard
                        key={asset.id}
                        asset={asset}
                    />
                ))}
            </div>
        </>
    );
}

export default Assets;