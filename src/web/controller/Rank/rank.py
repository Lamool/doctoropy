import random

포켓몬번호 = [1,2,3,4,5,6,7,8,9,10,11,12]

라운드 = 1

while len(포켓몬번호) > 1:
    print(f"\n=== {라운드} 라운드 ===")
    이긴포켓몬 = []
    random.shuffle(포켓몬번호)

    for i in range(0, len(포켓몬번호) - 1, 2):
        대결 = [포켓몬번호[i], 포켓몬번호[i + 1]]
        print(f"누가 이길까요? {대결[0]} vs {대결[1]}")
        승자선택 = int(input("이기는 쪽을 선택하세요 (1 또는 2): "))
        승자 = 대결[승자선택 - 1]
        이긴포켓몬.append(승자)

    print("남은 사람들", 이긴포켓몬)
    포켓몬번호 = 이긴포켓몬
    라운드 += 1

print(f"\n최종 승자는 {포켓몬번호[0]} 입니다!")

#포켓몬 번호 csv에서 받아오기
#포켓몬번호 리스트에 저장
#선택된 포켓몬 DB조회수 1씩 증가
#최종 승리된 포켓몬 승리회수 1증가
#승리한 포켓몬 값만 출력페이지 전달