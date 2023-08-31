context('Search', () => {
  describe('Search a list of authors', () => {
    beforeEach(() => {
      cy.viewport(1600, 1200)
    })

    it('User can search', () => {
      cy.intercept(
        {
          pathname: '/api/author/search',
          method: 'GET',
          query: { 'team_size': '6', q: 'A test prompt' }
        },
        {
          statusCode: 200,
          body: [
            {
              fullName: 'Leonard Hofstadter',
              orcid: '0000-0000-0000-0001',
              university: 'Princeton University'
            }
          ]
        }
      ).as('searchAuthors')

      cy.visit('/')
      cy.contains(/lorem ipsum/i)
      cy.get('#q').type('A test prompt')
      cy.get('button').click()

      cy.wait('@searchAuthors')

      cy.location('pathname').should('eq', '/team')
      cy.contains('Leonard Hofstadter')
    })
  })
})
