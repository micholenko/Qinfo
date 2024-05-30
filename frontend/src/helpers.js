import { useStudyStore } from '@/stores/study'

const studyStore = useStudyStore()

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

const fetchUsers = async (studyId) => {
    const response = await fetch(`http://localhost:5000/users?studyId=${studyId}`)
    const data = await response.json()
    studyStore.participants = data
    console.log('studyStore.participants:', studyStore.participants)
  }
  
  const fetchQset = async (qsetId) => {
    let ret = await fetch(`http://localhost:5000/qsets/${qsetId}`)
    const data = await ret.json()
    console.log(data)
    studyStore.cards = data
  }
  
export const fillStudyStore = async (studyId) => {
    let ret = await fetch(`http://localhost:5000/studies/${studyId}`)
    const data = await ret.json()
  
    await fetchUsers(studyId)
    await fetchQset(data.qset_id)
    studyStore.distribution = data.distribution
    studyStore.positions = data.col_values
    studyStore.rounds = data.rounds
    studyStore.id = studyId
    studyStore.title = data.title
    studyStore.description = data.description
    studyStore.question = data.question
    studyStore.created_time = data.created_time
  }