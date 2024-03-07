export const cardsWithText = (qsort, qset) => {
    console.log('qsort', qsort)
    console.log('qset', qset)
    let qsortWithText = qsort.map((row, i) => {
        return row.map((id, j) => {
            return qset.find(q => q.id === id).text
        })
    }
    )
    return qsortWithText
} 