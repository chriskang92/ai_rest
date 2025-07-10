from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.forms import ValidationError


class Article(models.Model):
    title = models.CharField(
        max_length=100, db_index=True
    )  # db_index=Trueallowsforfasterlookups
    preview_image = models.ImageField(
        upload_to="articles/", blank=True, null=True
    )  # 필로우설치가필수/데이터가없을수도있으므로NullandBlankaresettoTrue
    content = models.TextField()
    show_at_index = models.BooleanField(
        default=True
    )  # DefaultisTrue,soarticlesareshownatindexbydefault
    is_published = models.BooleanField(
        default=False
    )  # DefaultisFalse,soarticlesarenotpublishedbydefault
    created_at = models.DateTimeField(
        "생성일", auto_now_add=True
    )  # Automaticallysetthefield
    modified_at = models.DateTimeField(
        "수정일", auto_now=True
    )  # Automaticallysetthefield

    class Meta:
        verbose_name = "칼럼"
        verbose_name_plural = "칼럼s"  # verbosemeans"morereadablename"

    def __str__(self):
        return f"{self.id}-{self.title}"  # itisshownasastringintheadminpanel


class Restaurant(models.Model):
    name = models.CharField(
        "이름", max_length=100, db_index=True
    )  # db_index=Trueallowsforfasterlookups
    branch_name = models.CharField(
        "지점", max_length=100, null=True, blank=True, db_index=True
    )  # db_index=Trueallowsforfasterlookups
    description = models.TextField(
        "설명", null=True, blank=True
    )  # nullandblankaresettoTrue,sothefieldcanbeempty
    address = models.CharField(
        "주소", max_length=255, null=True, blank=True
    )  # nullandblankaresettoTrue,sothefieldcanbeempty
    feature = models.CharField(
        "특징", max_length=255, null=True, blank=True
    )  # nullandblankaresettoTrue,sothefieldcanbeempty
    is_closed = models.BooleanField(
        "폐업여부", default=False
    )  # DefaultisFalsesorestaurantsarenotclosedbydefault
    latitude = models.DecimalField(
        "위도", max_digits=16, decimal_places=12, db_index=True, default="0.0000"
    )  # max_digit는소수점포함전체숫자
    longitude = models.DecimalField(
        "경도", max_digits=16, decimal_places=12, db_index=True, default="0.0000"
    )  # 소수점이하자릿수12
    phone = models.CharField(
        "전화번호", max_length=20, help_text="E.164포맷", null=True, blank=True
    )  # nullandblankaresettoTrue,sothefieldcanbeempty
    rating = models.DecimalField("평점", max_digits=3, decimal_places=2, default="0.0")
    rating_count = models.PositiveIntegerField("좋아요 개수", default=0)
    start_time = models.TimeField("영업시작시간", null=True, blank=True)
    end_time = models.TimeField("영업종료시간", null=True, blank=True)
    last_order_time = models.TimeField("라스트오더시간", null=True, blank=True)
    category = models.ForeignKey(
        "RestaurantCategory",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,  # 참조된 카테고리 삭제시 Null로 설정 (데이터 보)
    )
    tags = models.ManyToManyField(
        "Tag", blank=True
    )  # 레스토랑과 다대다 관계를 설정, 빈 값 허용
    region = models.ForeignKey(
        "restaurant.Region",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="지역",
        related_name="restaurants",
    )  # 레스토랑 지역 region.restaurants.all()로 접근 가능

    class Meta:
        verbose_name = "레스토랑"
        verbose_name_plural = "레스토랑s"

    def __str__(self):
        return f"{self.name}{self.branch_name}" if self.branch_name else f"{self.name}"


class CuisineType(models.Model):
    name = models.CharField("음식 종류", max_length=100, db_index=True)

    class Meta:
        verbose_name = "음식 종류"
        verbose_name_plural = "음식 종류s"

    def __str__(self):
        return self.name


class RestaurantCategory(models.Model):
    name = models.CharField("카테고리 이름", max_length=100, db_index=True)
    cuisineType = models.ForeignKey(
        "CuisineType",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="음식 종류",
        related_name="restaurant_categories",
    )
    # 음식 종류와 외래키 관계 설정

    class Meta:
        verbose_name = "레스토랑 카테고리"
        verbose_name_plural = "레스토랑 카테고리s"

    def __str__(self):
        return self.name


class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(
        "Restaurant", on_delete=models.CASCADE, related_name="images"
    )  # 레스토랑과 일대다 관계 설정
    is_representative = models.BooleanField(
        "대표 이미지 여부", default=False
    )  # 이미지 업데이트 했는데 체크하면 대표이미지로 설정, 따라서 BooleanField 사용
    order = models.PositiveIntegerField(
        "순서", null=True, blank=True
    )  # 이미지 순서 지정, PositiveIntegerField 사용
    name = models.CharField(
        "이미지 이름", max_length=100, null=True, blank=True
    )  # 이미지 이름, null과 blank 허용
    image = models.ImageField(
        "이미지",
        max_length=100,
        upload_to="restaurant_images",
        null=True,
        blank=True,
    )  # 이미지 파일 업로드 경로 설정 / 이미지도 글자로 인식하기 때문에 max_length 설정
    # 사용자가 이미질 업로드하면 Media_root/restaurant_images/ 폴더 아래 이미지가 저장됌.
    created_at = models.DateTimeField(
        "생성일", auto_now_add=True, db_index=True
    )  # 생성일 자동 설정
    updated_at = models.DateTimeField(
        "수정일", auto_now=True, db_index=True
    )  # 수정일 자동 설정

    class Meta:
        verbose_name = "레스토랑 이미지"
        verbose_name_plural = "레스토랑 이미지들"

    def __str__(self):
        return f"{self.id}:{self.image}"

    # 대표이미지를 2개 이상 지정하지 못하도록 막는 코드를 작성
    def clean(self):
        images = self.restaurant.restaurantimage_set.filter(is_representative=True)
        # .restaurantimage_set는 RestaurantImage 모델의 related_name을 사용하여 레스토랑에 연결된 이미지들을 가져옴
        # .filter(): 괄호 안의 조건에 맞는 이미지들만 가져옴
        if self.is_representative and images.exclude(id=self.id).count() > 0:
            raise ValidationError("대표 이미지는 하나만 지정할 수 있습니다.")

    # 현재 이미지가 대표이미지고 현재 이미지를 제외한 다른 이미지가 1개 이상 존재한다면 ValidationError를 발생시킴
    # images.exclude(id=self.id)로 현재 이미지를 제외한 나머지 이미지들을 가져오고, 그 개수가 0보다 크면 ValidationError를 발생시킴
    # ValidationError는 Django에서 제공하는 예외 클래스, raise로 예외를 발생시킴
    # 이 코드는 레스토랑 이미지가 저장되기 전에 clean() 메서드가 호출되어 검증을 수행함
    # 만약 대표 이미지가 2개 이상 지정되면 ValidationError가 발생하여 저장이 되지 않음


class RestaurantMenu(models.Model):
    restaurant = models.ForeignKey(
        "Restaurant", on_delete=models.CASCADE, related_name="menus"
    )  # 레스토랑과 일대다 관계 설정
    name = models.CharField(
        "메뉴 이름", max_length=100, db_index=True
    )  # 메뉴 이름, db_index=True로 빠른 검색 가능
    price = models.PositiveIntegerField(
        "가격", default=0
    )  # 메뉴 가격, 기본값은 0, 음수 정수는 불가
    image = models.ImageField(
        "메뉴 이미지", upload_to="restaurant_menus", null=True, blank=True
    )  # Media_root/restaurant_menus 폴더에 이미지 저장
    created_at = models.DateTimeField(
        "생성일", auto_now_add=True, db_index=True
    )  # 생성일 자동 설정 (조회 속도를 빠르게 하기 위해서)
    updated_at = models.DateTimeField(
        "수정일", auto_now=True, db_index=True
    )  # 수정일 자동 설정

    class Meta:
        verbose_name = "레스토랑 메뉴"
        verbose_name_plural = "레스토랑 메뉴s"

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.CharField("리뷰 제목", max_length=100)
    author = models.CharField(
        "작성자", max_length=50, null=True, blank=True
    )  # 작성자 이름, null과 blank 허용
    profile_image = models.ImageField(
        "프로필 이미지",
        upload_to="review_profiles",
        null=True,
        blank=True,
    )  # 프로필 이미지 업로드 경로 설정
    content = models.TextField("리뷰 내용")  # 리뷰 내용
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], default=1
    )  # 평점, 1~5 사이의 정수
    # 양의 정수만 허용되는 필드로 값의 범위를 0-9로 제한
    Restaurant = models.ForeignKey(
        "Restaurant", on_delete=models.CASCADE, related_name="reviews"
    )
    social_channel = models.ForeignKey(
        "SocialChannel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviews",
    )  # 소셜 채널과 외래키 관계 설정
    created_at = models.DateTimeField(
        "생성일", auto_now_add=True, db_index=True
    )  # 생성일 자동 설정
    updated_at = models.DateTimeField(
        "수정일", auto_now=True, db_index=True
    )  # 수정일 자동 설정

    class Meta:
        verbose_name = "리뷰"
        verbose_name_plural = "리뷰s"

    def __str__(self):
        return f"{self.author}:{self.title}"


class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(max_length=100, upload_to="review")
    created_at = models.DateTimeField("생성일", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField("수정일", auto_now=True, db_index=True)

    class Meta:
        verbose_name = "리뷰이미지"
        verbose_name_plural = "리뷰이미지"

    def str(self):
        return f"{self.id}:{self.image}"


class SocialChannel(models.Model):
    name = models.CharField("이름", max_length=100)

    class Meta:
        verbose_name = "소셜채널"
        verbose_name_plural = "소셜채널"

    def str(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        "이름", max_length=100, unique=True
    )  # 이 필드는 중복을 허용하지 않음

    class Meta:
        verbose_name = "태그"
        verbose_name_plural = "태그"

    def str(self):
        return self.name


class Region(models.Model):
    sido = models.CharField("광역시도", max_length=20)
    sigungu = models.CharField("시군구", max_length=20)
    eupmyeondong = models.CharField("읍면동", max_length=20)

    class Meta:
        verbose_name = "지역"
        verbose_name_plural = "지역"
        unique_together = ("sido", "sigungu", "eupmyeondong")

    def str(self):
        return f"{self.sido} {self.sigungu} {self.eupmyeondong}"
