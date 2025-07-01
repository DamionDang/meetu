// src/components/MapComponent.js
import React, { useEffect, useRef } from 'react';

const MapComponent = ({ userLocation, nearbyUsers, posts }) => {
    const mapRef = useRef(null);

    useEffect(() => {
        if (!mapRef.current) return;

        // 初始化地图
        const map = new window.google.maps.Map(mapRef.current, {
            center: userLocation || { lat: 37.7749, lng: -122.4194 },
            zoom: 13,
        });

        // 显示当前用户位置
        if (userLocation) {
            new window.google.maps.Marker({
                position: userLocation,
                map,
                title: "You are here",
                icon: {
                    path: window.google.maps.SymbolPath.CIRCLE,
                    scale: 8,
                    fillColor: "#00ff00",
                    fillOpacity: 1,
                    strokeColor: "#000",
                    strokeWeight: 2,
                },
            });
        }

        // 显示附近用户
        nearbyUsers.forEach((user) => {
            new window.google.maps.Marker({
                position: { lat: user.latitude, lng: user.longitude },
                map,
                title: user.username,
                label: user.username,
            });
        });

        // 显示动态标记
        posts.forEach((post) => {
            new window.google.maps.Marker({
                position: { lat: post.latitude, lng: post.longitude },
                map,
                title: post.content.slice(0, 30),
                icon: "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png",
            });
        });

    }, [userLocation, nearbyUsers, posts]);

    return <div ref={mapRef} style={{ height: "100vh", width: "100%" }} />;
};

export default MapComponent;