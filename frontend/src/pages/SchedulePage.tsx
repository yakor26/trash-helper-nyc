import { useEffect, useState } from "react";
import BasicLayout from "../components/BasicLayout"
import { useAuth } from "../context/AuthContext"
import { Box, Heading, Text } from "@chakra-ui/react";
import { FaToggleOff, FaToggleOn } from "react-icons/fa";
import { IoLocation } from "react-icons/io5";
import { apiAuth } from "../utils/api";
import type { AxiosResponse } from "axios";
import type { Schedule } from "../utils/helper";


export default function SchedulePage() {
    const { user } = useAuth();
    const addresses = user?.addresses
    const [schedules, setSchedules] = useState<Schedule[]>();
    useEffect(() => {
        const getSchedules = async () => {
        try {
            const responses = await Promise.all(addresses.map(async address => {
                return (await apiAuth.get(`/api/addresses/${address.id}/schedule`)).data;
            }))
            setSchedules(responses)
        } catch(error) {
            return error;
        }
    }
    getSchedules();
    }, [addresses])
    return (
        <>
        <BasicLayout>
        <Heading size={"lg"}>Sanitation Schedule</Heading>
        {addresses ? <Box>
        {addresses.map((address) =>
        <Box>
            <li key={address.id}>
                {address.street_address}, {address.city}, {address.state}, {address.zip_code}
            </li> 
        
        </Box>
        )}
        </Box>
        : <p>Address: No address saved yet</p>}
        {schedules && <Box>
            {schedules.map((schedule) => 
            <Box>
                <p>Trash Collection Days: {schedule.days_trash} </p>
                <p>Recycling Collection Days: {schedule.days_recycling}</p>
                <p>Compost Collection Days: {schedule.days_compost}</p>
                <p>Large Items Collection Days: {schedule.days_large_items}</p>
            </Box>
        )}
        </Box>}
        
        </BasicLayout>
        </>

    )
}