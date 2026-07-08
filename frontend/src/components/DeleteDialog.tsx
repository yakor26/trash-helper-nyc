import { Button, IconButton, AlertDialog, AlertDialogOverlay, AlertDialogBody, AlertDialogContent, AlertDialogHeader, AlertDialogFooter, useDisclosure } from "@chakra-ui/react";
import type { Address } from "../utils/helper";
import { useRef } from "react";
import type { Dispatch, SetStateAction } from "react";
import { apiAuth } from "../utils/api";
import { FaTrashAlt } from "react-icons/fa";

type DeleteDialogProps = {
    address: Address;
    addresses: Address[];
    setAddresses: Dispatch<SetStateAction<Address[]>>;
}

export function DeleteDialog({ address, addresses, setAddresses }: DeleteDialogProps) {
    const { isOpen, onOpen, onClose } = useDisclosure();
    const cancelRef = useRef(null);
    const handleDeleteAddress = async (address_id: number) => {
        try {
            await apiAuth.delete(`/api/addresses/${address_id}`);
            const updatedAddresses = addresses.filter(prev => prev.id !== address_id)
            setAddresses(updatedAddresses)
            onClose();
        } catch(error) {
            console.log(error);
        }
    }
    return (
    <>
    <IconButton
        position={"absolute"}
        right={2}
        top={2}
        aria-label="delete"
        icon={<FaTrashAlt/>}
        color={"red.700"}
        bg={"gray.200"}
        onClick={onOpen}
    />
    <AlertDialog
    isOpen={isOpen}
    leastDestructiveRef={cancelRef}
    onClose={onClose}
    >
    <AlertDialogOverlay>
        <AlertDialogContent maxWidth={"2xl"} bg={"brand.white.100"}>
            <AlertDialogHeader fontSize='xl' fontWeight='bold'>
                Delete Address
            </AlertDialogHeader>
            <AlertDialogBody fontSize={"lg"}>
                {`Are you sure you want to delete this address? 
                ${address.street_address}, ${address.city}, ${address.state}, ${address.zip_code}. 
                You cannot undo this action.`}
            </AlertDialogBody>
            <AlertDialogFooter>
                <Button ref={cancelRef} onClick={onClose}>
                    Cancel
                </Button>
                <Button colorScheme='red' onClick={() => {handleDeleteAddress(address.id)}} ml={3}>
                    Delete
                </Button>
            </AlertDialogFooter>
        </AlertDialogContent>
    </AlertDialogOverlay>
    </AlertDialog>
    </>
)}