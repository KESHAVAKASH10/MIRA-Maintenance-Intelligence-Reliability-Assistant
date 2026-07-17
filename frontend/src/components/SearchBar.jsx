function SearchBar({ placeholder }) {
    return (
        <input
            type="text"
            placeholder={placeholder}
            className="w-full border rounded-lg px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
        />
    );
}

export default SearchBar;