import { useState } from 'react'

function Counter() {

    let [counter, setCounter] = useState(0)

    const Increment = () => {
        setCounter(counter + 1)
    }

    const Decrement = () => {
        setCounter(counter - 1)
    }

    return (
        <div className='flex justify-center items-center h-full flex-col'>
            <h1 className=' text-2xl font-bold'>BytesCode | Vivek Kumar</h1>
            <h3 className=' mt-2 text-xl'>Counter Value: <span className='rounded-md font-bold bg-red-200 py-0 px-1'>{counter}</span></h3>
            <div className='grid grid-cols-2 gap-4 mt-4'>
                <button onClick={Decrement} className=' bg-amber-400 rounded-md py-1 px-2 cursor-pointer'>Decrement</button>
                <button onClick={Increment} className=' bg-amber-400 rounded-md py-1 px-2 cursor-pointer'>Increment</button>
            </div>
        </div>
    )
}

export default Counter
