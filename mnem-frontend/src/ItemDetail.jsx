import React, { useEffect, useState, useParams } from "react";
import { getItem } from "./services/items";

export default function ItemDetail() {
    const [item, setItem] = useState(null);
    const { id } = useParams();
    useEffect(() => {
        const fetchItems = async () => {
            setItem(await getItem(id));
        }
        fetchItems();
    }, [id]);
    return (
        <div>
            <h2>Item Detail</h2>
            {item ? (
                <div>
                    <p>Name: {item.name}</p>
                    <p>Price: {item.price}</p>
                    <p>Weight: {item.weight}</p>
                </div>
            ) :
                <p>Loading...</p>}
        </div>
    )
}